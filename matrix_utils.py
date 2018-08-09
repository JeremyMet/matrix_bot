from matrix_client.client import MatrixClient ;
from matrix_client.api import MatrixRequestError
import json ;
import time ;
import re ;
import datetime
import threading ;
import sys

class matrix_utils(object):


    def __init__(self, config_path = "config.json"):
        self.rooms = {} ;
        self.room_timer = set() ;
        self.is_timer_on = False
        self.is_on = False ;
        try:
            with open(config_path) as f:
                self.config = json.loads(f.read());
        except IOError as e:
            print(e) ;
        self.login = self.config["login"] ;
        self.password = self.config["password"] ;
        try:
            self.client = MatrixClient(self.config["host"])
            self.client.login_with_password(self.login, self.password) ;
        except MatrixRequestError as e:
            print(e)
            sys.exit() ;

    def add_service_to_room(self, room, service_name, service):
        dic = self.rooms[room][1] ;
        if not(service_name in dic):
            dic[service_name] = service ;
        else:
            raise("Service already does already exist.")

    def remove_service_from_room(self, room, service_name):
        dic = self.rooms[room][1];
        if service_name in dic:
            del dic[service_name] ;
        else:
            raise("Service {} does not exist.".format(service_name)) ;


    def add_room(self, room_name):
        new_room = self.client.join_room(room_name) ;
        listener = new_room.add_listener(self.callback) ;
        self.rooms[new_room] = (room_name,  {}, listener);
        new_room.send_text(self.config["bot_start_txt"]) ;
        return new_room ;


    def remove_room(self, room):
        if room in self.room_timer and self.is_timer_on:
            raise("Can not leave rooms while timer is on.") ;
        if room in self.rooms:
            uuid = self.rooms[room][2]
            self.client.remove_listener(uuid);
            del self.rooms[room] ;
            room.leave() ;
        else:
            raise("Room {} does not exist.".format(str(room))) ;


    def callback(self, room, event):
        if event["type"] == "m.timer":
            for service in self.rooms[room][1].values():
                service.clock_update() ;
                ret = service.run_on_clock() ;
                if ret:
                    room.send_text(ret) ;
        if event["type"] == "m.room.message":
            login = re.search("@[aA-zZ]+[0-9]*", event["sender"]).group(0) ;
            login = login[1:] ;
            print(">>> " + str(room) + " at " + str(datetime.datetime.now())+ " by "+login);
            if login != self.login:
                text = str(event["content"]["body"]) ;
                if text == self.config["bot_down_cmd"]:
                    room.send_text(self.config["bot_stop_txt"]);
                    self.exit() ;
                if self.rooms:
                    for service in self.rooms[room][1].values():
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
        event = {};
        event["type"] = "m.timer"
        while(self.is_timer_on):
            if self.is_on:
                for room in self.room_timer.copy():
                    self.callback(room, event);
            time.sleep(t)

    def start_timer(self, t = 1):
        if not(self.is_timer_on):
            self.is_timer_on = True ;
            t1 = threading.Thread(target=self.timer_callback, args=(t,))
            t1.start();

    def stop_timer(self):
        self.is_timer_on = False ;

    def add_timer_to_room(self, room):
        if not(room in self.room_timer):
            self.room_timer.add(room) ;
        else:
            raise("Room {} does already have a timer.".format(str(room))) ;

    def remove_timer_from_room(self, room):
        if room in self.room_timer:
            print("Deleting Tick Channel {}".format(str(room))) ;
            self.room_timer.remove(room) ;

    def exit(self):
        for room_key, room in self.rooms.items():
            for service_name, service in room[1].copy().items():
                service.exit();
                self.remove_service_from_room(room_key, service_name) ;
            self.remove_timer_from_room(room_key) ;
            # room_key.leave() ;
        self.is_timer_on = False ;
        self.is_on = False ;