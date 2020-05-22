from modules.module import module ;
from .mastermind import mastermind
import re
import unidecode


class mastermind_bot(module):

    def __init__(self, keyword = "mastermind", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.module_name = "mastermind"
        self.whatis = "A simple Mastermind Game."
        self.__version__ = "0.0.1"
        self.mastermind_inst = mastermind()


    @module.login_check_dec # ignore when messages come from the bot itself.
                            # it can be useful to listen to what the bot says in some cases
    def process_msg_active(self, cmd, sender, room):
        return ""

    #@module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        #match = re.findall('\§([a-zA-Z]+)', (unidecode.unidecode(cmd)))
        if cmd[0] == '§' and self.mastermind_inst.check_proposition_consistency(cmd[1:]):
            self.reset_clock();
            return self.mastermind_inst.propose(cmd[1:]) ;


    @module.module_on_dec
    def run_on_clock(self):
        # <- Your code goes here.
        pass

    def exit(self):
        # <- Your code goes here.
        # This function is called when the bot is shut down,
        # this can for instance be used to save temporary variables into files.
        pass
