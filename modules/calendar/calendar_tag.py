from datetime import datetime;

class calendar_tag(object):

    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    day_int = lambda x : x.replace("%day_int", str(datetime.now().day));
    month_int = lambda x : x.replace("%month_int", str(datetime.now().month));

    day_str = lambda x : x.replace("%day_str", calendar_tag.days[datetime.weekday(datetime.now())]);
    month_str = lambda x : x.replace("%month_str", calendar_tag.months[(datetime.now().month)-1]);

    year_int = lambda x : x.replace("%year_int", str(datetime.now().year));

    tags_func = [day_int, month_int, day_str, month_str, year_int];


    @classmethod
    def apply_tag(cls, current_str):
        ret = current_str;
        for tags in cls.tags_func:
            ret = tags(ret);
        return ret;
