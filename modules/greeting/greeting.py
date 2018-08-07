import random ;

class greeting(object):

    greeting_array = ["salut", "coucou", "hello", "hola", "demat", "pouet", "pwet"] ;
    tbot_array = ["tbot", "tersabot", "tersa_bot"] ;

    def __init__(self):
        pass

    def run(self, cmd, sender):
        cmd = cmd.lower() ;
        cmd_array = cmd.split(" ")
        if len(cmd_array) == 2:
            if cmd_array[0] in greeting.greeting_array and cmd_array[1] in greeting.tbot_array:
                return random.choice(greeting.greeting_array).capitalize()+" "+sender.capitalize()+" \o/" ;

    def exit(self):
        pass ;




if __name__ == "__main__":

    greet = greeting() ;
    print(greet.run("salut tbot", "Tersaken")) ;

