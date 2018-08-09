from modules.module import module ;
import datetime ;
import json ;
import random ;

class quotes(module):

    def __init__(self):
        super().__init__() ;
        self.keywords = ["quotes"] ; # <- Name of your module
        self.help = "A quote module" ; # <- will be printed out by the admin module
        self.whatis = "A simple quote module !"
        self.__version__ = "0.0.1"
        self.last_day = 0 ;
        try:
            with open("modules/quotes/quotes.json", "r") as f:
                self.quotes = json.loads(f.read()) ;
        except IOError:
            raise("Could not load the quotes file \"quote.json\"") ;

    @module.module_on_dec
    @module.check_command_dec # can be commented for passive functions.
    def run(self, cmd, sender=None, room=None):
        # if self.check_command(cmd):
        #     return None ; Comment should be removed for passive functions
        # <- Your code goes here.
        return "Today's Quote : \n \"" + self.current_quote["quote"] + "\" by " + self.current_quote["name"];

    @module.module_on_dec
    @module.clock_dec
    def run_on_clock(self):
        current_time = datetime.datetime.now().day ;
        if current_time > self.last_day:
            self.current_quote = random.choice(self.quotes) ;
            self.last_day = current_time ;
            return "Today's Quote : \n \""+self.current_quote["quote"]+"\" by "+self.current_quote["name"] ;
