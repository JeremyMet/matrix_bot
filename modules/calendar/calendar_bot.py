from modules.module import module ;
from .calendar import calendar;
from datetime import datetime;
import re;

class calendar_bot(module):

    filter_regex = re.compile("\(@filter:#[0-9aA-zZ]+:[0-9aA-zZ]+.[0-9aA-zZ]{1,5}\)");

    @classmethod
    def get_filters(cls, msg):
        ret_filter_list = [];
        mt_iter = re.finditer(cls.filter_regex, msg);
        for mt in mt_iter:
            current_filter = mt.group(0);
            msg = msg.replace(current_filter, "");
            ret_filter_list.append(current_filter[9:-1]);
        return ret_filter_list, msg;

    def __init__(self, keyword = "calendar", event_file_path="modules/calendar/event_file.dic"): # <- template ... Here goes your default module name
        super().__init__(keyword) ;
        self.help = "WIP" ; # <- will be printed out by the admin module
        self.whatis = "A Calendar module. "
        self.module_name = "Calendar Module"
        self.__version__ = "0.0.1"
        self.calendar_inst = calendar();

    @module.module_on_dec
    @module.login_check_dec
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
    @module.login_check_dec
    def process_msg_passive(self, cmd, sender=None, room=None):
        ret = self.calendar_inst.parse(cmd);
        return ret;

    # @module.login_check_dec
    @module.module_on_dec
    @module.clock_dec
    @module.lock_dec
    def run_on_clock(self, room):
        ret = "";
        ret_array = self.calendar_inst.get_event_array();
        current_alias = room.current_alias;
        # let us filter out !
        if ret_array:
            for msg in ret_array:
                msg_filter, clear_msg = calendar_bot.get_filters(msg) ;
                print("msg_filter ", msg_filter)
                if msg_filter: # if there is a filter, have to check if room belongs to it
                    if current_alias in msg_filter:
                        ret += clear_msg+'\n';
                else: # there is no filter, then send the msg as a whole
                    ret += msg+'\n'
        return ret;

    def exit(self):
        print("\tSauvegarde en cours ...")
        ret = self.calendar_inst.save_event_dic();
