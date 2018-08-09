from modules.module import module ;

class template(module):

    def __init__(self):
        super().__init__() ;
        self.keywords = ["template"] ; # <- Name of your module
        self.help = "Useless module" ; # <- will be printed out by the admin module
        self.whatis = "A simple template !"
        self.__version__ = "0.0.1"

    @module.module_on_dec
    @module.check_command_dec # can be commented for passive functions.
    def run(self, cmd, sender=None, room=None):
        # if self.check_command(cmd):
        #     return None ; Comment should be removed for passive functions
        # <- Your code goes here.
        pass

    @module.module_on_dec
    @module.clock_dec
    def run_on_clock(self):
        # <- Your code goes here.
        pass