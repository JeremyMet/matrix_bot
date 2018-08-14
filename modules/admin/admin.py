
from modules.module import module ;
import urllib
import importlib
import os ;
import shutil ;
import re ;

# TODO When uninstalling a service, check if it is not used in another room and then delete it.(should we ?)

class admin(module):

    def __init__(self, keyword = "admin", is_permanent = True):
        super().__init__(keyword, is_permanent) ;
        if not(os.path.isdir("./tmp_modules")):
            os.makedirs("./tmp_modules") ;
        self.modules_to_be_installed = [] ;
        self.instruction_stack = [] ;


    def list_rooms(self):
        ret = "" ;
        for room_name in self.caller.rooms.values():
            ret += "- "+room_name[0]+"\n"
        return ret[:-1] ;

    def list_services(self, room):
        room_item = self.caller.rooms[room][1] ;
        ret = ""
        for service in room_item:
            ret+="- "+service.keywords[0]+" version "+service.__version__
            if service.is_module_activated():
                ret+=" [x]"
            else:
                ret+=" [ ]"
            ret+="\n" ;
        return ret[:-1] ;

    # def activate_service(self, service_name, room):
    #     room_item = self.caller.rooms[room] ;
    #     services = room_item[1] ;
    #     if service_name in services:
    #         services[service_name].set_module_on() ;
    #         return "Service {} is activated.".format(service_name) ;
    #     else:
    #         return "Service {} does not exist.".format(service_name) ;
    #
    # def deactivate_service(self, service_name, room):
    #     room_item = self.caller.rooms[room] ;
    #     services = room_item[1] ;
    #     if service_name in services:
    #
    #         services[service_name].set_module_off() ;
    #         return "Service {} is deactivated.".format(service_name) ;
    #     else:
    #         return "Service {} does not exist".format(service_name) ;


    def install_from_list(self, url, room = None):
        modules_to_be_installed = urllib.request.urlopen(url).read().decode("utf-8").split("\n") ;
        for module in modules_to_be_installed:
            instruction = module.split("==") ;
            if room:
                self.instruction_stack.append("tbot admin install {} {} {} \ntbot admin pop".format(instruction[0], instruction[1], room)) ;
            else:
                self.instruction_stack.append("tbot admin install {} {} \ntbot admin pop".format(instruction[0], instruction[1])) ;
            print(self.instruction_stack)
        return "tbot admin pop" ;


    def install_module(self, name, url, room):
        if name in self.caller.rooms[room][2]:
            return "Module {} does already exist.".format(name) ;
        try:
            module_name = re.search("/[0-9aA-zZ]+.py", url).group(0)[1:-3];
            fid = open("./tmp_modules/"+str(module_name)+".py", "w") ;
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
                new_module = importlib.import_module("tmp_modules."+module_name, package = None) ;
                class_ = getattr(new_module, module_name)
                class_.is_permanent = False ;
                is_ok = self.caller.add_service_to_room(room, class_(name) ) ;
        if is_ok:
            return "Module {} installed.".format(name)
        else:
            return "Too many services ({} nb services Max).".format(self.caller.__MAX_SERVICE__);



    def process_msg_active(self, cmd, sender = None, room = None):
        raw_args = cmd.split() ;
        if len(raw_args) >= 3:
            r2 = raw_args[2] ;
            if r2 == "push":
                print(">>> {}".format(cmd))
                tmp_re = re.findall('"(.*?)"', cmd) ;
                print(tmp_re) ;
                if tmp_re:
                    instruction = tmp_re[0] ;
                    self.instruction_stack.append(instruction) ;
                    return "Instruction \"{}\" added to stack".format(instruction) ;
                else:
                    return "No valid string found."
            if r2 == "pop":
                if self.instruction_stack:
                    instruction = self.instruction_stack.pop() ;
                    return instruction ;
                else:
                    return "Stack is empty" ;
            elif r2 == "room_list":
                return self.list_rooms() ;
            elif r2 == "service_list":
                return self.list_services(room)
            # elif r2 == "service_on":
            #     if len(raw_args) == 4: return self.activate_service(raw_args[3], room) ;
            #     else:
            #         return "Unknown Room."
            # elif r2 == "service_off":
            #     if len(raw_args) == 4: return self.deactivate_service(raw_args[3], room) ;
            elif r2 == "install":
                if len(raw_args) == 5: return self.install_module(raw_args[3], raw_args[4], room) ;
                if len(raw_args) == 6:
                    if raw_args[5] in self.caller.room_name_to_room:
                        other_room = self.caller.room_name_to_room[raw_args[5]] ;
                        return self.install_module(raw_args[3], raw_args[4], other_room) ;
            elif r2 == "install_from_list":
                if len(raw_args) == 4: return self.install_from_list(raw_args[3]) ;
                if len(raw_args) == 5: return self.install_from_list(raw_args[3], raw_args[4]) ;


    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        pass

    @module.module_on_dec
    def run_on_clock(self):
        if self.modules_to_be_installed:
            pass

    def exit(self):
        if os.path.isdir("./tmp_modules"):
            shutil.rmtree("./tmp_modules") ;