
from modules.module import module ;
import urllib
import importlib
import os ;
import shutil ;
import re ;

class admin(module):

    def __init__(self):
        super().__init__() ;
        self.keywords = ["admin"] ;
        if not(os.path.isdir("./tmp_modules")):
            os.makedirs("./tmp_modules") ;


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
        if name in self.caller.rooms[room][1]:
            return "Module {} does already exist.".format(name) ;
        try:
            fid = open("./tmp_modules/"+str(name)+".py", "w") ;
        except IOError as e:
            print(e)
        else:
            try:
                file = urllib.request.urlopen(url).read() ;
            except Exception as e:
                print(e)
                return "url content is not a valid python script."
            else:
                fid.write(file.decode("utf-8")) ;
                fid.close() ;
                module_name = re.search("/[0-9aA-zZ]+.py", url).group(0)[1:-3] ;
                new_module = importlib.import_module("tmp_modules."+module_name, package = None) ;
                class_ = getattr(new_module, module_name)
                is_ok = self.caller.add_service_to_room(room, name, class_() ) ;
        if is_ok:
            return "Module {} installed.".format(name)
        else:
            return "Too many services."


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

    def exit(self):
        if os.path.isdir("./tmp_modules"):
            shutil.rmtree("./tmp_modules") ;



