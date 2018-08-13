from matrix_client.client import MatrixClient ;
from matrix_client.api import MatrixRequestError
import json ;
import time ;
import re ;
import datetime
import threading ;
import sys


class matrix_utils(object):

    __MAX_SERVICE__ = 32 ; # Number of services that can be simultaneously installed.


    def __init__(self, config_path = "config.json"):
        self.rooms = {} ;
        self.room_name_to_room = {}
        self.services = {} ;
        self.services_sensitive_on_clock = set() ;
        self.is_timer_on = False
        self.is_on = False ;
        self.nb_current_service = 0 ;
        # self.logger.setLevel(logging.DEBUG) ;
        try:
            with open(config_path) as f:
                self.config = json.loads(f.read());
        except IOError as e:
            print(e) ;
        self.login = self.config["login"] ;
        self.password = self.config["password"] ;
        try:
            self.client = MatrixClient(self.config["host"])
            self.client.login(self.login, self.password) ;
        except MatrixRequestError as e:
            print(e)
            sys.exit() ;

    def add_service_to_room(self, room, service, message_on_start = None):
        if self.nb_current_service < matrix_utils.__MAX_SERVICE__:
            tmp_set_service = self.rooms[room][1] ;
            tmp_set_service_name = self.rooms[room][2] ;
            service_name = service.keywords[0] ;
            if not(service in tmp_set_service) and not(service_name in tmp_set_service_name):
                self.rooms[room][1].add(service);
                self.rooms[room][2].add(service_name) ;
                self.nb_current_service +=1 ;
                if not(service in self.services):
                    self.services[service] = set() ;
                self.services[service].add(room) ;
                if message_on_start:
                    room.send_text(message_on_start) ;
                return True
            else:
                raise Exception("Service already does already exist.")
        else:
            # raise Exception("Maximum number of services ({}) reached".format(str(matrix_utils.__MAX_SERVICE__))) ;
            return False

    def remove_service_from_room(self, room, service):
        tmp_set_service = self.rooms[room][1];
        tmp_set_service_name = self.rooms[room][2];
        if service in tmp_set_service:
            tmp_set_service.remove(service) ;
            tmp_set_service_name.remove(service.keywords[0]) ;
            self.nb_current_service -= 1;
        else:
            raise Exception("Service {} does not exist.".format(service)) ;


    def add_room(self, room_name, message_on_start = None):
        new_room = self.client.join_room(room_name) ;
        listener = new_room.add_listener(self.callback) ;
        self.rooms[new_room] = (room_name, set(), set(),  listener);
        self.room_name_to_room[room_name] = new_room ;
        if message_on_start:
            new_room.send_txt()
        else:
            new_room.send_text(self.config["bot_start_txt"]) ;
        return new_room ;


    def remove_room(self, room):
        if room in self.room_timer and self.is_timer_on:
            raise Exception("Can not leave rooms while timer is on.") ;
        if room in self.rooms:
            uuid = self.rooms[room][3]
            self.client.remove_listener(uuid);
            room_name = self.rooms[room][0] ;
            del self.room_name_to_room[room_name] ;
            del self.rooms[room] ;
            room.leave() ;
        else:
            raise Exception("Room {} does not exist.".format(str(room))) ;


    def callback(self, room, event):
        if event["type"] == "m.room.message":
            login = re.search("@[aA-zZ]+[0-9]*", event["sender"]).group(0) ;
            login = login[1:] ;
            tmp_log = "Event from " + str(self.rooms[room][0]) + " at " + str(datetime.datetime.now())+ " by "+login ;
            print(tmp_log)
            text = str(event["content"]["body"]) ;
            if text == self.config["bot_down_cmd"]:
                room.send_text(self.config["bot_stop_txt"]);
                self.exit() ;
            if self.rooms:
                for service in self.rooms[room][1].copy():
                    service.admin(self) ;
                    ret = service.run(text, login, room) ;
                    if ret:
                        room.send_text(ret) ;

    def spawn(self):
        self.client.start_listener_thread()
        self.is_on = True ;
        print("Ready ...")
        while(self.is_on):
            time.sleep(0.5)

    def timer_callback(self, t):
        while(self.is_timer_on):
            if self.is_on:
                for service in self.services_sensitive_on_clock.copy():
                    service.clock_update() ;
                    ret = service.run_on_clock() ;
                    for room in self.services.copy()[service]:
                        if ret:
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
        for room_key, room in self.rooms.items():
            for service in room[1].copy():
                print(service) ;
                service.exit();
                # self.remove_service_from_room(room_key, service) ;
            # room_key.leave() ;

    def add_timer_to_service(self, service):
        if not(service in self.services_sensitive_on_clock):
            self.services_sensitive_on_clock.add(service) ;

    def remove_timer_from_service(self, service):
        if service in self.services_sensitive_on_clock:
            self.services_sensitive_on_clock.remove(service) ;
        else:
            raise BaseException("Service {} is not clock sensitive.".format(service)) ;