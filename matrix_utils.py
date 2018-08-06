from matrix_client.client import MatrixClient ;
from matrix_client.api import MatrixRequestError
import json ;
import time ;
import re ;
from pendu_bot import pendu_bot



class matrix_utils(object):


    def __init__(self, config_path = "config.json"):
        self.rooms = [] ;
        try:
            with open(config_path) as f:
                config = json.loads(f.read());
        except IOError as e:
            print(e) ;
        self.login = config["login"] ;
        self.password = config["password"] ;
        try:
            self.client = MatrixClient(config["host"])
            self.client.login_with_password(self.login, self.password) ;
            self.rooms.append(self.client.join_room(config["room"])) ;
            self.rooms[0].add_listener(self.echo)
            self.rooms[0].send_text("Tersa_bot à votre service !")
        except MatrixRequestError as e:
            print(e)
        self.services = [] ;


    def add_service(self, service):
        self.services.append(service) ;

    def add_room(self, room):
        self.rooms.append(room)



    def echo(self, room, event):
        print("Event")
        if event["type"] == "m.room.message":
            login = re.search("@[aA-zZ]+[0-9]*", event["sender"]).group(0) ;
            login = login[1:]
            if login != self.login:
                text = str(event["content"]["body"]) ;
                print("debug "+str(text))
                for service in self.services:
                    if text.split(" ")[0] == "bot":
                        ret = service.run(text.split(" ")[2:]) ;
                    # else:
                    #     ret = service.run(text) ;
                    print(ret)
                    if ret:
                        self.rooms[0].send_text(ret)


    def spawn(self):
        self.client.start_listener_thread()
        print("Ready ...")
        while(True):
            time.sleep(0.1)



if __name__ == "__main__":

    matrix_obj = matrix_utils() ;
    my_pendu = pendu_bot() ;
    matrix_obj.add_service(my_pendu)
    matrix_obj.spawn() ;

