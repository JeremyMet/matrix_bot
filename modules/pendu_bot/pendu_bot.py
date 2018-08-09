import json
import random
import re
import unidecode
from .pendu import pendu
from modules.module import module ;

class pendu_bot(module):


    def __init__(self):
        super().__init__() ;
        self.keywords = ["pendu"] ;
        self.help = "type tbot pendu help for further details.";
        self.whatis = "Un simple jeu du pendu."
        self.__version__ = "0.0.1"
        self.pendu = pendu() ;

    # def process(self, cmd):
    # 	match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
    # 	if match:
    # 		return self.pendu.propose(match[1])
    # 	return None

    @module.module_on_dec
    # @module.check_command_dec
    def run(self, cmd, sender = None, room = None):
        match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
        if match:
            return self.pendu.propose(match.group(0)[1])
        args = cmd.split(" ") ;
        args = args[2:] # used for retro-compatibily
        if not(self.check_command(cmd)):
            return None ;
        if len(args)<1:
            return ;
        if args[0] == "propose":
            if len(args)>1:
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
        return None ;

    @module.module_on_dec
    @module.clock_dec
    def run_on_clock(self):
        if self.get_timer() > 7200:
            self.reset_clock() ;
            return "Rappel ! \n "+str(self.pendu) ;


    def exit(self):
        self.pendu.save_score() ;
        print("Service "+str(self)+" was stopped.") ;


if __name__ == "__main__":
    pb = pendu_bot() ;
