from modules.module import module ;
import datetime ;
import json ;
import random ;

# This module has been written in a old fashion way.
# You should follow modules/template.py as a template for your own module :-)

class quotes(module):

    def __init__(self, keyword = "quotes", is_permanent = False):
        super().__init__(keyword, is_permanent) ;
        self.keywords = ["quotes"] ; # <- Name of your module
        self.help = "A quote module" ; # <- will be printed out by the admin module
        self.whatis = "A simple quote module !"
        self.__version__ = "0.0.1"
        self.last_time = datetime.date(1961, 1, 1) ;
        self.ret = "" ;
        try:
            with open("modules/quotes/stupidstuff.json", "r") as f:
                self.quotes = json.loads(f.read()) ;
        except IOError:
            raise("Could not load the quotes file \"quote.json\"") ;

    @module.module_on_dec
    @module.check_command_dec # can be commented for passive functions.
    @module.login_check_dec
    def run(self, cmd, sender=None, room=None):
        raw_args = cmd.split() ;
        if len(raw_args) >= 3:
            if raw_args[2] == "uninstall":
             return self.remove(room) ;
        else:
            if not(self.ret):
                self.run_on_clock() ;
            return self.ret ;

    @module.module_on_dec
    def run_on_clock(self):
        current_time = datetime.datetime.now() ;
        if current_time.day != self.last_time.day:
            current_time_str = datetime.date(current_time.year, current_time.month, current_time.day).isoformat() ;
            current_quote_index = (pow(current_time.day+current_time.month+current_time.year, 2)+current_time.day)%len(self.quotes) ;
            self.current_quote = self.quotes[current_quote_index] ;
            while(not(self.current_quote)):
                current_quote_index += 1 ;
                self.current_quote = self.quotes[current_quote_index] ;
            self.last_time = current_time ;
            self.ret = "~~~ Today's Joke (" +  current_time_str +") ~~~ \n" \
                   +self.current_quote["body"] +'\n'+'\t'*10+ "Category "+self.current_quote["category"] ;
            return self.ret ;
