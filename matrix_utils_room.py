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

    def timer_callback(self, t):
        format_to_html = lambda s : s.replace("\n", "<br>").replace("\t", "&emsp;");
        while(self.is_timer_on):
            time.sleep(t)
            for room_id in self.room_dic:
                room = self.room_dic[room_id].room_obj;
                for service in self.room_dic[room_id].service_set:
                    if service.is_clock_sensitive():
                        service.clock_update() ;
                        ret = service.run_on_clock(room) ;
                        if ret: # should return a string
                            ret = ret.replace("\n", "<br>");
                            ret = ret.replace("\t", "&emsp;");
                            room.send_html(ret, msgtype="m.notice");

    def start_timer(self, t = 1):
        if not(self.is_timer_on):
            self.is_timer_on = True ;
            t1 = threading.Thread(target=self.timer_callback, args=(t,))
            t1.start();

    def stop_timer(self):
        self.is_timer_on = False ;

    @lock_dec
    def exit(self):
        self.is_timer_on = False ;
        self.is_on = False ;
        service_ret_buffer = {}
        for room_id in self.room_dic:
            room = self.room_dic[room_id].room_obj;
            service_set = self.room_dic[room_id].service_set;
            for service in service_set:
                if not(service in service_ret_buffer):
                    print("Module {} {} {} is shutting down.".format(bcolors.OKGREEN, service.module_name, bcolors.ENDC)) ;
                    ret = service.exit();
                    service_ret_buffer[service] = ret;
                else:
                    ret = service_ret_buffer[service];
                if ret:
                    room.send_html(ret, msgtype="m.notice");
        # for room in self.room_dic:
            # room.send_text(self.config["bot_stop_txt"]);
        sys.exit() ;

    def error_handle(self, err):
        print("Server is not {} responding {} ({}). Restarting ...".format(bcolors.FAIL, bcolors.ENDC, err));
        self.exit();
