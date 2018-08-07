import json
import random
import re
import unidecode
from .pendu import pendu

#TODO MODULE NAME

class pendu_bot:
	def __init__(self):
		self.keywords = ["pendu"]
		self.pendu = pendu() ;



	# def process(self, cmd):
	# 	match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
	# 	if match:
	# 		return self.pendu.propose(match[1])
	# 	return None

	def run(self, cmd):
		match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
		if match:
			return self.pendu.propose(match.group(0)[1])
		if cmd.split(" ")[0] != "tbot":
			return None ;
		args = cmd.split(" ")[2:]
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
			return "bot pendu propose A pour proposer la lettre A \n bot pendu show" ;
		elif args[0] == "event":
			return self.pendu.show_event() ;
		return None ; 


	def exit(self):
		self.pendu.save_score() ;
		return "Service "+str(self)+"arrêté."


if __name__ == "__main__":
	pb = pendu_bot() ; 
