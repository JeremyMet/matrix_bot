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

## TODO When adding a timer, check it is instantiated somhere ... ;-)

class matrix_utils_ext(object):

    __MAX_SERVICE__ = 32 ; # Number of services that can be simultaneously installed.
    room_tuple = namedtuple("room_tuple", "room_addr listener")

    def __init__(self, config_path = "config.json"):
        self.room_dic = {} ;
        self.services_sensitive_on_clock = set() ;
        self.is_timer_on = False
        self.is_on = False ;
        self.nb_current_service = 0 ;
        self.service_list = [];
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

    def add_service_to_room(self, room, service, message_on_start = None):
        ret = False;
        if self.nb_current_service < matrix_utils_ext.__MAX_SERVICE__:
            service.add_room(room);
            self.service_list.append(service);
            ret = True;
        else:
            #raise Exception("Maximum number of services ({}) reached".format(str(matrix_utils.__MAX_SERVICE__))) ;
            pass;
        return ret;

    def remove_service_from_room(self, room, service):
        ret = False;
        if service.remove_room(room):
            ret = True;
            # if service is not linked to any room, remove from service_list
            if not(service.get_room_list()):
                if (service in self.service_list):
                    room.send_text(service.exit());
                    index = self.service_list.index(service);
                    self.service_list.pop(index);
        else:
            #raise Exception("Service {} does not exist in room {}.".format(service, room)) ;
            pass;
        return ret;

# TODO ; eventuellement vérifier si une room avec une même adresse n'existe pas ?
    def add_room(self, room_addr, message_on_start = False):
        room = self.client.join_room(room_addr) ;
        listener = room.add_listener(self.callback) ;
        self.room_dic[room] = matrix_utils_ext.room_tuple(room_addr, listener) # (room object address, room_name (room address), listener object)
        if message_on_start:
            room.send_text(self.config["bot_start_txt"]) ;
        return room ;

    def remove_room(self, room):
        if not(room in self.room_dic):
            return False;
        for service in service_list:
            if (room in service.get_room_list()):
                # there are still some services linked to room.
                return False;
        listener = self.room_dic[room].listener;
        self.client.remove_listener(listener);
        room.leave() ;
        del self.room_dic[room];
        return True;

    def callback(self, room, event):
        if event["type"] == "m.room.message":
            login = re.search("@[aA-zZ]+[0-9]*", event["sender"]).group(0) ;
            login = login[1:] ;
            tmp_log = "Event from " + bcolors.OKGREEN + self.room_dic[room].room_addr + bcolors.ENDC + " at " + str(datetime.datetime.now())+ " by "+login ;
            print(tmp_log)
            text = str(event["content"]["body"]) ;
            ## Stop Service Management
            if text == self.config["bot_down_cmd"]:
                self.exit();
            ## Otherwise, run services
            for service in self.service_list:
                if (room in service.get_room_list()):
                    ret = service.run(text, login, room) ;
                    if ret:
                        room.send_text(ret) ;

    def spawn(self):
        self.client.start_listener_thread(exception_handler=self.error_handle);
        self.is_on = True ;
        print(bcolors.OKGREEN+
        "\n---------------------------------------------------\n"+
        "---- Matrix Bot v0.0.1 ----------------------------\n"+
        "---------------------------------------------------\n"+
        bcolors.ENDC)
        while(self.is_on):
            time.sleep(0.5)

    def timer_callback(self, t):
        while(self.is_timer_on):
            if self.is_on:
                for service in self.service_list:
                    if service.is_clock_sensitive():
                        service.clock_update() ;
                        ret = service.run_on_clock() ;
                        if ret:
                            for room in service.get_room_list():
                                room.send_text(ret) ;
            time.sleep(t)

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
        for room in self.room_dic:
            room.send_text(self.config["bot_stop_txt"]);
        sys.exit() ;

    def error_handle(self):
        print("Server is not {} responding {}. Restarting ...".format(bcolors.FAIL, bcolors.ENDC));
        self.exit();
