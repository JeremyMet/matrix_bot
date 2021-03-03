import json
import random
import re
import unidecode
from .pendu import pendu
from modules.module import module ;

class pendu_bot(module):


    def __init__(self, keyword = "pendu", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.module_name = "pendu_bot"
        self.help = "type tbot pendu help for further details.";
        self.whatis = "Un simple jeu du pendu."
        self.__version__ = "0.0.1"
        self.pendu = pendu() ;

    # def process(self, cmd):
    # 	match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
    # 	if match:
    # 		return self.pendu.propose(match[1])
    # 	return None

    def on_start(self):
        ret = "<b>\uD83E\uDDE0 ~~~ Jeu du Pendu ~~~ \uD83E\uDDE0</b> \n"+str(self.pendu);
        return ret;

    # @module.module_on_dec
    @module.login_check_dec
    # @module.check_command_dec
    def process_msg_active(self, cmd, sender = None, room = None):
        args = cmd.split(" ") ;
        args = args[2:] # used for retro-compatibily
        if not(self.check_command(cmd)):
            return None ;
        if len(args)<1:
            return ;
        if args[0] == "propose":
            if len(args)>1:
                self.reset_clock() ;
                return self.pendu.propose(unidecode.unidecode(args[1])) ;
            else:
                return self.pendu.propose("") ;
        elif args[0] == "show":
            return str(self.pendu) ;
        elif args[0] == "score":
            return self.pendu.show_score() ;
        elif args[0] == "letters":
            return self.pendu.show_lt() ;
        elif args[0] == "debug":
            return "debug \n" ;
        elif args[0] == "words":
            return self.pendu.get_word_list();
        elif args[0] == "help":
            return "tbot pendu propose A pour proposer la lettre A, \n \
tbot pendu show montre l'état actuel du mot, \n \
tbot pendu event montre l'event en cours (s'il y en a)";
        elif args[0] == "event":
            return self.pendu.show_event() ;
        return "" ;

    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        match = re.fullmatch('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
        if match:
            self.reset_clock();
            current_prop = match[0];
            return self.pendu.propose(current_prop[1:]) ;


    @module.module_on_dec
    def run_on_clock(self, room=None):
        if self.get_timer() > 36000: # 10 hours.
            self.reset_clock() ;
            return "\u26A0\uFE0F Rappel ! \n \n "+self.pendu.show_lt()+"\n"+str(self.pendu) ;


    def exit(self):
        self.pendu.save_score() ;
        if self.pendu.lt:
            return "\u26A0\uFE0F Oooh Non ! Vous avez été trop lent \U0001F606 ! Le mot cherché était \"<b>{}</b>\".".format(self.pendu.current_word);
        else:
            return None;



if __name__ == "__main__":
    pb = pendu_bot() ;
