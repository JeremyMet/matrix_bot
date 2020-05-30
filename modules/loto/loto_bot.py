import random ;
from modules.module import module ;
from .loto import loto;
import datetime;

class loto_bot(module):

    def __init__(self, keyword = "loto", hour=0, minute=0): # <- template ... Here goes your default module name
        super().__init__(keyword) ;
        self.help = "propose (1,2,3,4,5,6)" ; # <- will be printed out by the admin module
        self.whatis = "A simple hello module. "
        self.__version__ = "0.0.1"
        self.loto_inst = loto();
        self.loto_inst.set_draw_time(hour, minute);

    @module.module_on_dec
    def run(self, cmd, sender=None, room=None):
        raw_cmd = cmd.split(" ");
        if (len(raw_cmd) == 3 and raw_cmd[2] == "get_dailybet"):
            ret = self.loto_inst.get_dailybet();
        elif (len(raw_cmd) == 3 and raw_cmd[2] == "get_scoreboard"):
            ret = self.loto_inst.get_scoreboard();
        else:
            ret = self.loto_inst.bet(sender, cmd);
        return ret ;


    @module.module_on_dec
    # @module.clock_dec
    def run_on_clock(self):
        log = self.loto_inst.get_log();
        draw_time = self.loto_inst.get_draw_time();
        last_draw = log["last_draw"];
        now = datetime.datetime.now();
        # Nous avons changé de jour ...
        delta = now-last_draw;        
        if delta.days > 0:
            if (draw_time.hour == now.hour and draw_time.minute == now.minute):
                ret = self.loto_inst.check_result();
                self.loto_inst.save_current_state();
                return ret;

    def exit(self):
        self.loto_inst.save_current_state();


if __name__ == "__main__":
    pass
