import json;
import random;
import datetime;
from collections import namedtuple;
import os.path
import pickle

Draw_Time = namedtuple("Draw_Time", "hour minute");

class loto(object):

    pt_table = {} ;
    pt_table[0] = 0 ;
    pt_table[1] = 1 ;
    pt_table[2] = 10 ;
    pt_table[3] = 100 ;
    pt_table[4] = 1000 ;
    pt_table[5] = 10000 ;
    pt_table[6] = 100000 ;

    def __init__(self, scoreboard_file="./modules/loto/scoreboard_file.dic", dailybet_file="./modules/loto/dailybet_file.dic", log_file = "./modules/loto/log.dic", nb_numbers=49, combination_length=6):
        self.scoreboard_file = scoreboard_file;
        self.dailybet_file = dailybet_file;
        self.log_file = log_file;
        self.nb_numbers = nb_numbers;
        self.combination_length = combination_length;
        self.scoreboard = {} ;
        self.dailybet = {} ;
        self.log = {} ;
        self.log["last_draw"] = datetime.datetime(1970, 1, 1);
        self.hour, self.minute = 0, 0;
        self.load_previous_state();

    def set_scoreboard_file(self, scoreboard_file):
        self.scoreboard_file = scoreboard_file;

    def set_log_file(self, log_file):
        self.log_file = log_file;

    def set_dailybet_file(self, dailybet_file):
        self.dailybet_file = dailybet_file;

    def set_draw_time(self, hour, minute):
        self.hour, self.minute = hour, minute;

    def get_draw_time(self):
        return Draw_Time(self.hour, self.minute);

    def get_log(self):
        return self.log;

    def load_previous_state(self):
        if os.path.isfile(self.scoreboard_file):
            with open(self.scoreboard_file, "rb") as json_file:
                self.scoreboard = pickle.load(json_file);
        if os.path.isfile(self.dailybet_file):
            with open(self.dailybet_file, "rb") as json_file:
                self.dailybet = pickle.load(json_file);
        if os.path.isfile(self.log_file):
            with open(self.log_file, "rb") as json_file:
                self.log = pickle.load(json_file);

    def save_current_state(self):
            with open(self.scoreboard_file, "wb") as json_file:
                pickle.dump(self.scoreboard, json_file);
            with open(self.dailybet_file, "wb") as json_file:
                pickle.dump(self.dailybet, json_file);
            with open(self.log_file, "wb") as json_file:
                pickle.dump(self.log, json_file);


    def draw(self):
        self.current_result = set();
        while(len(self.current_result) < self.combination_length):
            rd = random.randint(1, self.nb_numbers);
            self.current_result.add(rd);
        self.log["last_draw"] = datetime.datetime.now();
        #self.current_result = {1,2,3,8,33,2}; # todo remove!

    def check_result(self):
        self.draw(); # tirage
        ret = "\U0001F3B2 Les vainqueurs du {}. \nBravo à".format(datetime.datetime.today().strftime('%Y-%m-%d'));
        is_there_a_winner = False;
        for key, value in self.dailybet.items():
            tmp_nb_pt = len(self.current_result & value);
            if tmp_nb_pt > 0:
                is_there_a_winner = True;
                nb_pt = loto.pt_table[tmp_nb_pt];
                ret += "\n {} avec {} points ({} nombres corrects)".format(key, nb_pt, tmp_nb_pt)
                if key in self.scoreboard.keys():
                    self.scoreboard[key] += nb_pt;
                else:
                    self.scoreboard[key] = nb_pt;
        if is_there_a_winner:
            return ret;
        else:
            return "Pas de vainqueurs aujourd'hui ({}) !".format(datetime.datetime.today().strftime('%Y-%m-%d'));

    def bet(self, sender, proposition):
        # check if proposition is well-formed
        proposition = proposition.replace(" ", "");
        if (proposition[0] != "(" or proposition[-1] != ")"):
            return "";
        proposition = proposition[1:-1];
        proposition_array = proposition.split(",");
        if (len(proposition_array) != self.combination_length):
            return "La combinaison doit être de longueur {}.".format(self.combination_length);
        proposition_array = [(int(i) if (int(i) < self.nb_numbers) else 0) for i in proposition_array];
        if (0 in proposition_array):
            return "Les valeurs doivent être inférieures ou égales à {}.".format(self.nb_numbers);
        # proposition is well-formed,
        self.dailybet[sender] = set(proposition_array);
        return "La proposition {} de {} a bien été prise en compte.".format(self.dailybet[sender], sender);

    def get_dailybet(self):
        ret = "\U0001F3B2 Joueurs Participants - Grille";
        for key, value in self.dailybet.items():
            ret = "{}\n - {}: {} ".format(ret, key, value);
        return ret;

#todo mettre dans l'ordre croissant
    def get_scoreboard(self):
        ret = "\U0001F3B2 Tableau des Scores :";
        for key_value in sorted(self.scoreboard.items(), key=lambda x: x[1], reverse=True):
            ret = "{}\n\t - {}: {}".format(ret, key_value[0], key_value[1]);
        return ret;