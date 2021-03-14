import random ;
from modules.module import module ;
from .loto import loto;
import datetime;
import pickle

class loto_bot(module):

    def __init__(self, keyword = "loto", flask_scoreboard = "./modules/loto/flask_scoreboard.dic", hour=0, minute=0): # <- template ... Here goes your default module name
        super().__init__(keyword) ;
        self.help = "propose (1,2,3,4,5,6)" ; # <- will be printed out by the admin module
        self.whatis = "A loto hello module. "
        self.module_name = "Loto Module"
        self.__version__ = "0.0.1"
        self.loto_inst = loto(hour=hour, minute=minute);
        self.flask_scoreboard_array = {}
        with open(flask_scoreboard, "rb") as pickle_file:
            self.flask_scoreboard_array = pickle.load(pickle_file);

    @module.module_on_dec
    def process_msg_active(self, cmd, sender=None, room=None):
        raw_cmd = cmd.split(" ");
        ret = "" ;
        if (len(raw_cmd) == 3 and raw_cmd[2] == "dailybet"):
            ret = self.loto_inst.get_dailybet();
        elif (len(raw_cmd) == 3 and raw_cmd[2] == "scoreboard"):
            ret = self.loto_inst.get_scoreboard();
        elif (len(raw_cmd) == 3 and raw_cmd[2] == "draw"):
                ret = self.loto_inst.check_result();
        return ret ;

    @module.module_on_dec
    def process_msg_passive(self, cmd, sender=None, room=None):
        ret = self.loto_inst.bet(sender, cmd);
        return ret;


    @module.module_on_dec
    # @module.clock_dec
    def run_on_clock(self, room=None):
        log = self.loto_inst.get_log();
        last_draw = log["last_draw"];
        last_draw_month = last_draw.month;
        now = datetime.datetime.now();
        # Nous avons changé de jour ...
        delta = now-last_draw;
        if delta.days > 0:
            ret = self.loto_inst.check_result();
            self.loto_inst.save_current_state();
            # Dans le cas où l'on change de mois,
            if (now.month != last_draw.month):
                pass
                #todo
            return ret;

    def exit(self):
        print("\tSauvegarde en cours ...")
        self.loto_inst.save_current_state();


if __name__ == "__main__":
    pass
