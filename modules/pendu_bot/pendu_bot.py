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
        elif args[0] == "help":
            return "tbot pendu propose A pour proposer la lettre A, \n \
tbot pendu show montre l'état actuel du mot, \n \
tbot pendu event montre l'event en cours (s'il y en a)";
        elif args[0] == "event":
            return self.pendu.show_event() ;
        return "" ;


    def process_msg_passive(self, cmd, sender, room):
        match = re.findall('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
        if match:
            self.reset_clock();
            return self.pendu.propose(match[0]) ;


    @module.module_on_dec
    def run_on_clock(self):
        if self.get_timer() > 36000: # 10 hours. 
            self.reset_clock() ;
            return "/!\ Rappel ! \n \n "+self.pendu.show_lt()+"\n"+str(self.pendu) ;


    def exit(self):
        self.pendu.save_score() ;


if __name__ == "__main__":
    pb = pendu_bot() ;
