import json
import random
import re
import unidecode
from pendu import pendu

class pendu_bot:
	def __init__(self):
		self.keywords = ["pendu"]
		self.pendu = pendu() ;



	def process(self, cmd):
		match = re.match('\!([a-zA-Z]+)', (unidecode.unidecode(cmd)))
		if match:
			return self.pendu.propose(match[1])
		return None

	def run(self, args):
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
		return


if __name__ == "__main__":
	pb = pendu_bot() ; 
