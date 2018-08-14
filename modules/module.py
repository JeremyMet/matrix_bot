import json ;


#TODO CLOCK SENSITIVE

class module(object):

    bot_cmd = "" ;

    def login_check_dec(function):
        def wrapper(*args, **kargs):
            if args[2] != args[0].caller.login:
                return function(*args, **kargs) ;
            else:
                return None ;
        return wrapper ;

    def clock_dec(function):
        '''
        Deprecated
        :return:
        '''
        def wrapper(*args, **kargs):
            if args[0].clock_sensitive:
                return function(*args, **kargs)
            else:
                return None
        return wrapper ;


    def module_on_dec(function):
        def wrapper(*args, **kargs):
            if args[0].is_module_on:
                return function(*args, **kargs)
            else:
                return None
        return wrapper ;

    def check_command_dec(function):
        '''
        Deprecated
        :return:
        '''
        def wrapper(*args, **kargs):
            s = args[0];
            raw_args = args[1].split() ;
            if len(raw_args) >= 2 and raw_args[0] == module.bot_cmd and raw_args[1] in s.keywords:
                if len(raw_args) == 3:
                    if raw_args[2] == "uninstall":
                        room = args[3];
                        return s.remove(room) ;
                return function(*args, **kargs) ;
            else:
                return None ;
        return wrapper ;

    def check_command(self, cmd):
        raw_cmd = cmd.split() ;
        return len(raw_cmd) >= 2 and raw_cmd[0] == module.bot_cmd and raw_cmd[1] in self.keywords ;


    def __init__(self, keyword = None, is_permanent = False):
        self.timer = 0 ;
        self.clock_sensitive = True ;
        self.is_module_on = True ;
        self.caller = None ;
        self.help = "" ;
        self.whatis = "" ;
        self.raw_args = [] ;
        self.is_permanent = is_permanent ;
        if keyword:
            self.keywords = [keyword] ;
        else:
            self.keywords = ["Default_Module_Name"] ;
        self.__version__ = "0.0.0"
        if not(module.bot_cmd):
            try:
                with open("./config.json", "r") as f:
                    config = json.loads(f.read()) ;
                module.bot_cmd = config["bot_cmd"] ;
            except IOError as e:
                print("Could not load config.json "+str(e)) ;
                module.bot_cmd = "tbot";

    @module_on_dec
    def run(self, cmd, sender = None, room = None):
        pass

    @module_on_dec
    def run_on_clock(self):
        pass

    def exit(self):
        pass

    @module_on_dec
    def clock_update(self):
        self.timer += 1 ;

    def reset_clock(self):
        self.timer = 0 ;

    def set_clock_sensitivity_on(self):
        self.clock_sensitive = True ;

    def set_clock_sensitivity_off(self):
        self.clock_sensitive = False ;

    def get_timer(self):
        return self.timer ;

    def is_module_activated(self):
        return self.is_module_on ;

    def set_module_on(self):
        self.is_module_on = True ;

    def set_module_off(self):
        self.is_module_on = False ;

    def admin(self, caller):
        self.caller = caller ;

    def remove(self, room):
        try:
            self.caller.remove_service_from_room(room, self) ;
        except Exception as e:
            return "Can not remove service {} from room".format(self.keywords[0]) ,
        else:
            return "Service {} removed.".format(self.keywords[0])



    def run(self, cmd, sender=None, room=None):
        instruction_set = cmd.split("\n") ;
        ret = "" ;
        for instruction in instruction_set:
            if instruction == self.caller.config["bot_down_cmd"]:
                room.send_text(self.caller.config["bot_stop_txt"]);
                self.caller.exit();
            raw_args = instruction.split() ;
            tmp = "" ;
            if len(raw_args) >= 2 and raw_args[0] == self.bot_cmd and raw_args[1] in self.keywords[0]:
                if self.is_module_activated():
                    tmp = self.process_msg_active(instruction, sender, room) ;
                # Module Management.
                if not(tmp):
                    tmp = "" ;
                    if len(raw_args) == 3 and raw_args[2] == "uninstall":
                        if self.is_permanent:
                            tmp += "Module {} can not be desinstalled.".format(self.keywords[0]) ;
                        else:
                            return self.remove(room)
                    if len(raw_args) == 3 and raw_args[2] == "activate":
                        if self.is_module_activated():
                            tmp+= "Module {} is already activated.".format(self.keywords[0]) ;
                        else:
                            self.set_module_on() ;
                            tmp += "Module {} is activated".format(self.keywords[0])
                    if len(raw_args) == 3 and raw_args[2] == "deactivate":
                        if not(self.is_module_activated()):
                            tmp+= "Module {} is already deactivated.".format(self.keywords[0]) ;
                        elif self.is_permanent:
                            tmp+=  "Module {} can not be deactivated.".format(self.keywords[0]) ;
                        else:
                            self.set_module_off() ;
                            tmp+= "Module {} is deactivated.".format(self.keywords[0]) ;
            else:
                if self.is_module_activated():
                    tmp = self.process_msg_passive(instruction, sender, room);
            if tmp:
                ret += tmp+'\n' ;
        return ret ;


if __name__ == "__main__":
    mod = module() ;
    mod.clock_update() ;
    print(mod.timer)
    mod.clock_sensitive_off() ;
    print(mod.timer)