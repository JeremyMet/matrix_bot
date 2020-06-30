from modules.module import module ;
from .calendar import calendar;
from datetime import datetime;

class calendar_bot(module):

        def __init__(self, keyword = "calendar", event_file_path="modules/calendar/event_file.dic"): # <- template ... Here goes your default module name
            super().__init__(keyword) ;
            self.help = "WIP" ; # <- will be printed out by the admin module
            self.whatis = "A Calendar module. "
            self.module_name = "Calendar Module"
            self.__version__ = "0.0.1"
            self.calendar_inst = calendar();

#TODO regarder la format TIME pour éviter de devoir retraiter la chaine dans la fonction get_time
        @module.module_on_dec
        def process_msg_active(self, cmd, sender=None, room=None):
            raw_cmd = cmd.split(" ");
            ret = "" ;
            if (len(raw_cmd) == 4 and raw_cmd[2] == "delete"):
                ret = self.calendar_inst.remove_event(raw_cmd[3]);
            if (len(raw_cmd) == 3 and raw_cmd[2] == "save"):
                ret = self.calendar_inst.save_event_dic();
            if (len(raw_cmd) == 3 and raw_cmd[2] == "get_events"):
                ret = self.calendar_inst.get_events();
            if (len(raw_cmd) == 3 and raw_cmd[2] == "get_time"):
                now = datetime.now()
                if now.minute>10:
                    ret = "\U0001f4c5 Il est {}:{}.".format(now.hour, now.minute);
                else:
                    ret = "\U0001f4c5 Il est {}:0{}.".format(now.hour, now.minute);
            return ret ;

        @module.module_on_dec
        def process_msg_passive(self, cmd, sender=None, room=None):
            ret = self.calendar_inst.parse(cmd);
            return ret;

        @module.module_on_dec
        # @module.clock_dec
        def run_on_clock(self):
            ret = self.calendar_inst.get_event_str();
            return ret;


        def exit(self):
            print("\tSauvegarde en cours ...")
            ret = self.calendar_inst.save_event_dic();
