import random ;
from modules.module import module ;

class greeting(module):

    greeting_array = ["salut", "coucou", "hello", "hola", "demat", "pouet", "pwet"] ;
    tbot_array = ["tbot", "tersabot", "tersa_bot"] ;
    tbot_random_sentences = \
    ["Pfff je m'ennuie", \
     "Ça va sinon ?", \
     "Il fait beau chez vous ?", \
     "Quelle puce m'a piqué ?", \
     "Jpp ..." \
     ]

    @module.module_on_dec
    def run(self, cmd, sender=None, room = None):
        cmd = cmd.lower() ;
        cmd_array = cmd.split(" ")
        if len(cmd_array) == 2:
            if cmd_array[0] in greeting.greeting_array and cmd_array[1] in greeting.tbot_array:
                return random.choice(greeting.greeting_array).capitalize()+" "+sender.capitalize()+" \o/" ;

    @module.module_on_dec
    @module.clock_dec
    def run_on_clock(self):
        if self.timer > 1800:
            self.reset_clock() ;
            return random.choice(greeting.tbot_random_sentences) ;




if __name__ == "__main__":

    greet = greeting() ;
    print(greet.run("salut tbot", "Tersaken")) ;

