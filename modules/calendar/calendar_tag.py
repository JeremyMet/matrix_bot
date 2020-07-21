from datetime import datetime;
import random;

class calendar_tag(object):

    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];
    months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
    day_int = lambda x : x.replace("%day_int", str(datetime.now().day));
    month_int = lambda x : x.replace("%month_int", str(datetime.now().month));
    day_str = lambda x : x.replace("%day_str", calendar_tag.days[datetime.weekday(datetime.now())]);
    month_str = lambda x : x.replace("%month_str", calendar_tag.months[(datetime.now().month)-1]);
    year_int = lambda x : x.replace("%year_int", str(datetime.now().year));


    @classmethod
    def generate_combination(cls, nb_numbers=49, combination_length=6):
        combination = set();
        while(len(combination)<combination_length):
            rd = random.randint(1, nb_numbers);
            combination.add(rd);
        combination_str = str(combination) ;
        combination_str = "("+combination_str[1:-1]+")" # removing brackets ;
        return combination_str;


    def loto_combination(current_str):
        if current_str.find("%loto") > 0:
            combination = calendar_tag.generate_combination();
            current_str = current_str[4:]; #remove tag
            current_str = current_str.replace("%loto", combination);
        return current_str;

    tags_func = [day_int, month_int, day_str, month_str, year_int, loto_combination];






    @classmethod
    def apply_tag(cls, current_str):
        ret = current_str;
        for tags in cls.tags_func:
            ret = tags(ret);
        return ret;
