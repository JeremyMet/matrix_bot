import json
import random
import re
import unidecode
from .pendu import pendu
from modules.module import module ;

class pendu_bot(module):


	def __init__(self):
		super().__init__() ;
		self.keywords = ["pendu"]
		self.pendu = pendu() ;

	# def process(self, cmd):
	# 	match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
	# 	if match:
	# 		return self.pendu.propose(match[1])
	# 	return None

	def run(self, cmd, sender = None):
		match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
		if match:
			return self.pendu.propose(match.group(0)[1])
		args = cmd.split(" ") ;
		if len(args) >= 1 and (args[0] != self.bot_cmd or not(args[1] in self.keywords)):
			return None ;
		args = args[2:] # used for retro-compatibily
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


	def run_on_clock(self):
		if self.timer > 28800:
			self.reset_clock() ;
			return "Rappel ! \n "+str(self.pendu) ;


	def exit(self):
		self.pendu.save_score() ;
		print("Service "+str(self)+"arrêté.") ;


if __name__ == "__main__":
	pb = pendu_bot() ; 
