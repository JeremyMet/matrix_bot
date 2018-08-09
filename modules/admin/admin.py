
from modules.module import module ;

class admin(module):

    def __init__(self):
        super().__init__() ;
        self.keywords = ["admin"] ;



    def list_services(self, room):
        room_item = self.caller.rooms[room] ;
        ret = ""
        for k_service, service in room_item[1].items():
            ret+="- "+k_service
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
            return "Service {} does not exist".format(service_name) ;

    def desactivate_service(self, service_name, room):
        room_item = self.caller.rooms[room] ;
        services = room_item[1] ;
        if service_name in services:
            services[service_name].set_module_off() ;
            return "Service {} is desactivated.".format(service_name) ;
        else:
            return "Service {} does not exist".format(service_name) ;




    @module.module_on_dec
    @module.check_command_dec
    def run(self, cmd, sender = None, room = None):
        raw_args = cmd.split() ;
        if len(raw_args) >= 3:
            r2 = raw_args[2] ;
            if r2 == "services":
                return self.list_services(room)
            if r2 == "service_on":
                if len(raw_args) >= 4:
                    return self.activate_service(raw_args[3], room) ;
            if r2 == "service_off":
                if len(raw_args) >= 4:
                    return self.desactivate_service(raw_args[3], room) ;