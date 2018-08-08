import json ;

class module(object):

    def __init__(self):
        self.timer = 0 ;
        try:
            with open("./config.json", "r") as f:
                config = json.loads(f.read()) ;
            self.bot_cmd = config["bot_cmd"] ;
        except IOError as e:
            print("Could not load config.json "+str(e)) ;
            self.bot_cmd = "tbot";

    def run(self, cmd, sender = None):
        pass

    def run_on_clock(self):
        pass

    def exit(self):
        pass

    def clock_update(self):
        self.timer += 1 ;

    def reset_clock(self):
        self.timer = 0 ;