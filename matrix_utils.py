from matrix_client.client import MatrixClient ;
from matrix_client.api import MatrixRequestError
import json ;
import time ;
import re ;
import threading ;


class matrix_utils(object):


    def __init__(self, config_path = "config.json"):
        self.rooms = {} ;
        self.rooms_name = {} ;
        self.room_timer = {} ;
        self.is_on = True ;
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
        self.services = [] ;


    def add_service_to_room(self, room, service_name, service):
        tmp_tuple = self.rooms[room] ;
        tmp_tuple[1][service_name] = service ;

    def remove_service_from_room(self, room, service_name):
        del self.rooms[room][1][service_name] ;

    def add_room(self, room_name):
        new_room = self.client.join_room(room_name) ;
        self.rooms[new_room] = (room_name,  {});
        self.rooms_name[room_name] = new_room ;
        new_room.add_listener(self.callback) ;
        new_room.send_text("TersaBot à votre service \o/ !") ;
        return new_room ;


    def remove_room(self, room_name):
        room = self.rooms_name[room_name] ;
        del self.rooms[room] ;
        del self.rooms_name[room_name] ;
        room.leave() ;


    def callback(self, room, event):
        print(">>> "+str(room))
        if event["type"] == "m.timer":
            room.send_text("Tick")
        if event["type"] == "m.room.message":
            login = re.search("@[aA-zZ]+[0-9]*", event["sender"]).group(0) ;
            login = login[1:]
            if login != self.login:
                text = str(event["content"]["body"]) ;
                if text == "tbot down":
                    room.send_text("TersaBot a été heureux d'avoir pu vous rendre service !");
                    self.exit() ;
                if self.rooms:
                    for service in self.rooms[room][1].values():
                        ret = service.run(text, login) ;
                        if ret:
                            room.send_text(ret) ;

    def spawn(self):
        self.client.start_listener_thread()
        print("Ready ...")
        while(self.is_on):
            pass 

    def timer_callback(self, room):
        while(room in self.room_timer):
            timer = self.room_timer[room] ;
            time.sleep(timer)
            event = {} ;
            event["type"] = "m.timer"
            self.callback(room, event) ;


    def add_timer(self, room, timer = 10):
        if not(room in self.room_timer):
            self.room_timer[room] = timer ;
            t1 = threading.Thread(target=self.timer_callback, args=(room,))
            t1.start() ;
        else:
            raise("Room {} does already have a timer.".format(str(room))) ;

    def remove_timer(self, room):
        if room in self.room_timer:
            print("Deleting Tick Channel")
            del self.room_timer[room] ;

    def exit(self):
        for room_key, room in self.rooms.items():
            for service_name, service in room[1].copy().items():
                service.exit();
                self.remove_service_from_room(room_key, service_name) ;
            self.remove_timer(room_key) ;
            room_key.leave() ;
        self.is_on = False ;

