

class wrapper_room(object):

    def __init__(room_obj, room_addr, room_listener):
        self.room_obj = room_obj ;
        self.room_addr = room_addr ;
        self.room_listener = room_listener ;

    def __str__(self):
        return self.room_name;

    def get_room_obj(self):
        return self.room_obj;

    def get_room_addr(self):
        return self.room_addr;

    def get_room_listener(self):
        return self.room_listener;
