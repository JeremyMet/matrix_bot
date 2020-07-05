# -*- coding: utf-8 -*-

from matrix_client.client import MatrixClient ;
from matrix_client.api import MatrixRequestError ;
import json ;
import time ;
import re ;
import datetime
import threading ;
import sys ;
from collections import namedtuple ;
from bcolors import bcolors ;
from modules.module import module;
from html_format import html_format;
from decorators import lock_dec;

## TODO When adding a timer, check it is instantiated somhere ... ;-)

class matrix_utils_room(object):

    __MODULE_NAME__ = "Matrix Bot"
    __VERSION__ = "v0.0.2a"

    __MAX_SERVICE__ = 32 ; # Number of services that can be simultaneously installed.
    filter_regex = re.compile("\(@filter:#[0-9aA-zZ]+:[0-9aA-zZ]+.[0-9aA-zZ]{1,5}\)");

    room_tuple = namedtuple("room_tuple", "room_obj, service_set")

    def __init__(self, config_path = "config.json"):
        self.room_dic = {} ;
        self.services_sensitive_on_clock = set() ;
        self.is_timer_on = False
        self.is_on = False ;
        self.nb_current_service = 0 ;
        self.service_list = {};
        # self.logger.setLevel(logging.DEBUG) ;
        try:
            with open(config_path) as f:
                self.config = json.loads(f.read());
        except IOError as e:
            print(e) ;
        self.login = self.config["login"] ;
        self.password = self.config["password"] ;
        module.config = self.config.copy();
        try:
            self.client = MatrixClient(self.config["host"])
            self.client.login(self.login, self.password) ;
        except MatrixRequestError as e:
            print(e)
            sys.exit() ;

    @lock_dec
    def add_service_to_room(self, room, service, message_on_start = None):
        ret = False;
        if self.nb_current_service < matrix_utils_room.__MAX_SERVICE__:
            room_id = room.room_id;
            self.room_dic[room_id].service_set.add(service);
            ret = True ;
        else:
            #raise Exception("Maximum number of services ({}) reached".format(str(matrix_utils.__MAX_SERVICE__))) ;
            pass;
        return ret;

    @lock_dec
    def remove_service_from_room(self, room, service):
        ret = False;
        room_id = room.room_id;
        if service in self.room_dic[room_id]:
            self.room_dic[room_id].service_set.remove(service);
            ret = True;
        else:
            #raise Exception("Service {} does not exist in room {}.".format(service, room)) ;
            pass;
        return ret;

# TODO ; eventuellement vérifier si une room redirige vers un même salon ...
    @lock_dec
    def add_room(self, room_addr, message_on_start = ""):
        room = self.client.join_room(room_addr) ;
        room.current_alias = room_addr;
        room_id = room.room_id;
        if not(room_id in self.room_dic):
            listener = room.add_listener(self.callback) ;
            self.room_dic[room.room_id] = matrix_utils_room.room_tuple(room, set())  # (room object address, room_name (room address), listener object)
            if message_on_start:
                # Conversion to HTML format
                message_on_start = message_on_start.replace("\n", "<br>");
                message_on_start = message_on_start.replace("\t", "&emsp;");
                room.send_html(message_on_start, msgtype="m.notice");
        else:
            room = None;
        return room ;

    @lock_dec
    def remove_room(self, room):
        room_id = room.room_id;
        if not(room_id in self.room_dic) or (self.room_dic[room_id].service_set):
            return False;
        room.leave() ;
        del self.room_dic[room_id];
        return True;

    @lock_dec # ??
    def callback(self, room, event):
        if event["type"] == "m.room.message":
            login = re.search("@[aA-zZ]+[0-9]*", event["sender"]).group(0) ;
            login = login[1:] ;
            room_id = room.room_id;
            tmp_log = "Event from " + bcolors.OKGREEN + room.current_alias + bcolors.ENDC + " at " + str(datetime.datetime.now())+ " by "+login ;
            print(tmp_log)
            text = str(event["content"]["body"]) ;
            ## Stop Service Management
            if text == self.config["bot_down_cmd"]:
                self.exit();
            ## Otherwise, run services
            room_id = room.room_id;
            for service in self.room_dic[room_id].service_set:
                ret = service.run(text, login, room) ;
                if ret:
                    for msg in ret:
                        # Conversion to HTML format
                        msg = msg.replace("\n", "<br>");
                        msg = msg.replace("\t", "&emsp;");
                        room.send_html(msg, msgtype="m.notice");

    def spawn(self):
        self.client.start_listener_thread(exception_handler=self.error_handle);
        self.is_on = True ;
        print(bcolors.OKGREEN+
        "\n---------------------------------------------------\n"+
        "---- Matrix Bot v0.0.2 ----------------------------\n"+
        "---------------------------------------------------\n"+
        bcolors.ENDC)
        while(self.is_on):
            time.sleep(1)

    @lock_dec # ??
    def timer_callback(self, t):
        while(self.is_timer_on):
            time.sleep(t)
            service_ret_buffer = {};
            if self.is_on:
                for room_id in self.room_dic:
                    room = self.room_dic[room_id].room_obj;
                    # print(room.current_alias)
                    for service in self.room_dic[room_id].service_set:
                        if service.is_clock_sensitive():
                            if not(service in service_ret_buffer):
                                service.clock_update() ;
                                ret = service.run_on_clock() ;
                                # Conversion to HTML format (+) filtering
                                if ret:
                                    ret = ret.replace("\n", "<br>");
                                    ret = ret.replace("\t", "&emsp;");
                                    filter_list, ret = matrix_utils_room.get_filter_header(ret);
                                else:
                                    filter_list = [] ;
                                service_ret_buffer[service] = (filter_list, ret);
                            else: # service is in service_ret_buffer;
                                filter_list, ret = service_ret_buffer[service][0], service_ret_buffer[service][1]
                        if ret: # if ret is not empty.
                            if filter_list:
                                if room.current_alias in filter_list and ret:
                                    room.send_html(ret, msgtype="m.notice");
                            else:
                                room.send_html(ret, msgtype="m.notice");

    def start_timer(self, t = 1):
        if not(self.is_timer_on):
            self.is_timer_on = True ;
            t1 = threading.Thread(target=self.timer_callback, args=(t,))
            t1.start();

    def stop_timer(self):
        self.is_timer_on = False ;

    def exit(self):
        self.is_timer_on = False ;
        self.is_on = False ;
        for service in self.service_list:
                print("Module {} {} {} is shutting down.".format(bcolors.OKGREEN, service.module_name, bcolors.ENDC)) ;
                tmp_msg = service.exit();
                if tmp_msg:
                    for room in service.get_room_list():
                        room.send_text(tmp_msg) ;
        # for room in self.room_dic:
            # room.send_text(self.config["bot_stop_txt"]);
        sys.exit() ;

    def error_handle(self, err):
        print("Server is not {} responding {} ({}). Restarting ...".format(bcolors.FAIL, bcolors.ENDC, err));
        self.exit();

    @classmethod
    def get_filter_header(cls, msg):
        ret_filter_list = [];
        mt_iter = re.finditer(cls.filter_regex, msg);
        for mt in mt_iter:
            current_filter = mt.group(0);
            msg = msg.replace(current_filter, "");
            ret_filter_list.append(current_filter[9:-1]);
        return ret_filter_list, msg;
