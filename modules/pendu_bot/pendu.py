## Pendu
## Authors : Bobbyblues, Tersaken

import random ;
import re ;
import json ;
import unidecode ;
import os ;

constant_life_max = 7 ;

class pendu(object):

    def __init__(self):
        # --- Score
        self.score = {} ;
        self.score["bot"] = 0 ;
        self.score["main"] = 0 ;
        # --- Event Management
        self.events = {} ;
        self.events_total_weight = 0 ;
        self.str_event = "" ;
        # --- Pendu Configuration
        self.life_max = 0 ;
        self.life = 0 ;
        self.lg = 0 ;
        self.mirror = False ;
        self.proba_event = 100 ; # Probabilité de trigger un event en pourcent (only integer).
        self.unauthorized_letters = [];
        # --- Inner State
        self.match = 0 ;
        self.lt = [] ;
        self.event_show = False ;

        self.regex_propose = re.compile('[a-zA-Z]{1}') ;
        self.min_lg = 5 ;
        self.max_lg = 30 ;
        self.conf = json.load(open("./modules/pendu_bot/config.json",'r')) ;
        #self.conf = json.load(open("sample_config.txt", 'r'));
        self.dico = [] ;
        with open(self.conf["dico_path"], 'r') as f:
            self.dico = f.readlines() ;
        if os.path.isfile(self.conf["score_path"]):
            with open(self.conf["score_path"], 'r') as f:
                self.score = json.load(f);
        for i in range(len(self.dico)):
            self.dico[i] = unidecode.unidecode(self.dico[i]) ;
        self.load_events() ;
        self.rst() ;

    def __str__(self):
        x = "" ;
        if self.str_event != "" and not(self.event_show):
            x += self.str_event ;
            self.event_show = True ;
        x += "\u270F\uFE0F Mot Courant : " ;
        if (self.mirror):
            iter = reversed(self.current_word) ;
        else:
            iter = self.current_word ;
        for c in iter:
            t = c+" " if c in self.lt else "_ " ;
            x+=t ;
        life_str = "\n\u2764\uFE0F Vie : "+"~"*(self.life_max-self.life)+"/)"+"~"*(self.life) + "\\o/~~\n";
        x+=life_str ;
        return x ;


    def rst(self):
        x = "" ;
        self.event_show = False ;
        self.lg = len(self.dico) ;
        self.lt = set() ;
        self.life_max = constant_life_max ;
        self.life = self.life_max ;
        self.match = 0 ;
        self.mirror = False ;
        self.unauthorized_letters = [];
        self.min_lg = 5 ;
        self.max_lg = 30 ;
        self.str_event = "" ;
        self.event_management() ;
        self.generate();


    def check(self):
        n = False ;
        x = "" ;
        if self.life < 0:
            nb_points = len(self.current_word)*3;
            self.score["bot"]+= nb_points  ;
            x = "\U0001f625 Vous avez perdu \U0001f625 ... Le Main est super mauvais (le bot gagne {} point(s)) \U0001f625\n".format(nb_points) ;
            x+= "Le mot recherché était \""+self.current_word+"\".\n" ;
            n = True ;
        if (self.match == len(self.current_word)):
            nb_points = len(self.current_word)+self.life+ len(set(self.current_word))-len(set(self.current_word).intersection(self.lt))
            self.score["main"]+= nb_points; # no overflow, python <3
            x = "\U0001f973 Vous avez gagné \U0001f973 ! Le mot recherché était effectivement \"{}\" ! Woah, vous êtes vraiment trop bons (+{} point(s)) !\n".format(self.current_word, nb_points) ;
            n = True ;
        if n:
            x += "  - Score du main : "+str(self.score["main"])+"\n" ;
            x += "  - Score du bot : "+str(self.score["bot"])+"\n" ;
            x += "Une nouvelle partie débute !! \n" ;
            self.rst() ;
        x+=str(self) ;
        return x ;


    def propose(self, lt):

        x = "" ;
        lt = lt.lower() ;
        lt = unidecode.unidecode(lt) ;
        if not(self.regex_propose.match(lt)):
            return "\u26A0\uFE0F Une lettre ou un mot sont demandés (en minuscules ou majuscules non accentuées) ! \n" ;
        if len(lt)>1: # il s'agit d'un mot.
            if len(lt) != len(self.current_word):
                return "\u26A0\uFE0F La taille du mot proposé n'est pas égale à celle du mot recherché !" ;
            if lt == self.current_word:
                self.match = len(self.current_word)
                x = self.check()
                return x
            else:
                self.life -= 1
                x = self.check()
                return x

        if self.unauthorized_letters:
            if lt in self.unauthorized_letters:
                x = "\u26A0\uFE0F Vous ne pouvez pas jouer la lettre \""+lt.capitalize()+"\" ...\n";
                return x ;

        if lt in self.lt:
            x = "\u26A0\uFE0F La lettre "+lt+" a déjà été proposée ! ...\n" ;
            return x ;
        else:
            self.lt.update(lt) ;
            if lt in self.current_word:
                self.match+=self.current_word.count(lt) ;
            else:
                self.life-=1 ;
            x = self.check() ;
            return x ;

    def show_lt(self):
        x = "Les lettres proposées sont :\n" ;
        x_ok = "" ; x_nok = "" ;
        for i in sorted(self.lt):
            if i in self.current_word:
                x_ok+=i+", " ;
            else:
                x_nok += i+", ";
        x_ok = x_ok[:-2] ;
        x_nok = x_nok[:-2] ; # gère tout seul la sortie de tableau
        x+= "- Retenue(s) : "+x_ok+"\n" ;
        x+= "- Non Retenue(s) : "+x_nok+"\n" ;
        return x ;

    def show_score(self):
            x = "" ;
            x += "  - Score du main : "+str(self.score["main"])+"\n" ;
            x += "  - Score du bot : "+str(self.score["bot"])+"\n" ;
            return x ;


    def generate(self):
        current_word = "" ;
        while(not(current_word) and (len(current_word) < self.min_lg or len(current_word) > self.max_lg)):
            r = random.randint(0, self.lg-1) ;
            attempt_word = self.dico[r][:-1]
            if re.fullmatch("^[a-zA-Z]+$", attempt_word):
                current_word = attempt_word;
        self.current_word = current_word ;

    def save_score(self):
        with open(self.conf["score_path"], 'w') as f:
            json.dump(self.score, f);


    ## Gestion des events


    def load_events(self):
        with open(self.conf["event_path"], 'r') as f:
            self.events = json.load(f) ;
        old_weight = 0 ;
        new_weight = 0 ;
        for key in self.events.keys():
            old_weight = new_weight ;
            new_weight = old_weight+self.events[key]["weight"] ;
            self.events[key]["proba_range"] = (old_weight, new_weight) ;
        self.events_total_weight = new_weight ;


    def event_management(self):
        dice_event_trigger = random.randint(0,99) ;
        if dice_event_trigger >= self.proba_event:
            return None ;
        dice_event_choice = random.randint(0, self.events_total_weight-1) ;
        for event in self.events.values():
            range = event["proba_range"] ;
            if range[0] <= dice_event_choice < range[1]:
                self.str_event = "\u26A0\uFE0F EVENT : "+str(event["message"])+'\n' ;
                self.life_max = constant_life_max+event["bonus_life"] ;
                self.life = constant_life_max+event["bonus_life"] ;
                self.mirror = True if event["mirror"] == "yes" else False ;
                self.min_lg = event["min_lg"] ;
                self.max_lg = event["max_lg"] ;
                self.unauthorized_letters = event["unauthorized_letters"] ;
                break ;

    def show_event(self):
        if (self.str_event == ""):
            return "\u26A0\uFE0F Aucun événement à afficher ... ";
        else:
            return self.str_event;

if __name__ == "__main__":
    P = pendu() ;
    print(P) ;
    while(True):
        A = input() ;
        print(P.propose(A)) ;
        print(P.show_lt()) ;
