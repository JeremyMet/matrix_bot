
from modules.module import module ;
import urllib
import importlib

class admin(module):

    def __init__(self):
        super().__init__() ;
        self.keywords = ["admin"] ;


    def list_rooms(self):
        ret = "" ;
        for room_name in self.caller.rooms.values():
            ret += "- "+room_name[0]+"\n"
        return ret[:-1] ;

    def list_services(self, room):
        room_item = self.caller.rooms[room] ;
        ret = ""
        for k_service, service in room_item[1].items():
            ret+="- "+k_service+" version "+service.__version__
            if service.is_module_activated():
                ret+=" [x]"
            else:
                ret+=" [ ]"
            ret+="\n" ;
        return ret[:-1] ;

    def activate_service(self, service_name, room):
        room_item = self.caller.rooms[room] ;
        services = room_item[1] ;
        if service_name in services:
            services[service_name].set_module_on() ;
            return "Service {} is activated.".format(service_name) ;
        else:
            return "Service {} does not exist.".format(service_name) ;

    def deactivate_service(self, service_name, room):
        room_item = self.caller.rooms[room] ;
        services = room_item[1] ;
        if service_name in services:
            services[service_name].set_module_off() ;
            return "Service {} is deactivated.".format(service_name) ;
        else:
            return "Service {} does not exist".format(service_name) ;

    def install_module(self, name, url, room):
        fid = open("./tmp_modules/"+str(name)+".py", "w") ;
        file = urllib.request.urlopen(url).read() ;
        fid.write(file.decode("utf-8")) ;
        fid.close() ;
        new_module = importlib.import_module("tmp_modules."+name, package = None) ;
        class_ = getattr(new_module, name)
        self.caller.add_service_to_room(room, name, class_() ) ;
        return "Module {} installed.".format(name)


    @module.module_on_dec
    @module.check_command_dec
    def run(self, cmd, sender = None, room = None):
        raw_args = cmd.split() ;
        if len(raw_args) >= 3:
            r2 = raw_args[2] ;
            if r2 == "room_list":
                return self.list_rooms() ;
            if r2 == "service_list":
                return self.list_services(room)
            elif r2 == "service_on":
                if len(raw_args) >= 4: return self.activate_service(raw_args[3], room) ;
            elif r2 == "service_off":
                if len(raw_args) >= 4: return self.deactivate_service(raw_args[3], room) ;
            elif r2 == "install":
                if len(raw_args) >= 5: return self.install_module(raw_args[3], raw_args[4], room) ;



