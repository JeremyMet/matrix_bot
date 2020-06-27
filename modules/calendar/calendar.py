#-*- coding: utf8 -*-
from enum import Enum, auto;
from datetime import datetime;
import re;
from collections import namedtuple;


class event_type(Enum):
    T = auto();
    DT = auto();
    MDT = auto();
    YMDT = auto();
    ERROR = auto();

class calendar(object):

    # date_regex = re.compile("\[[0-9]+(-(1[0-2])|(0?[1-9]))?(-[0-3]?[0-9])?( (([0-1]?[0-9]|2[0-3]):[0-5][0-9]))?\]\&\".+\""); # not perfect but should be ok.
    YMD_regex = re.compile("([0-9]+-(((1[0-2]))|(0?[1-9]))-((3[0-1])|([0-2]?[0-9])))|((((1[0-2]))|(0?[1-9]))-(3[0-1])|([0-2]?[0-9]))|((3[0-1])|([0-2]?[0-9]))");
    time_regex = re.compile("(([0-1]?[0-9])|(2[0-3])):[0-5][0-9]");
    datetime_type = namedtuple("datetime_type", "type datetime");


    def __init__(self, event_type, datetime_obj):
        self.event_type = event_type ;
        self.datetime_obj = datetime_obj;

    @classmethod
    def extract_time(cls, datetime_str):
        pass # regex here ;)

    @classmethod
    def parse_YMDT(cls, datetime_str):
        # TODO faire des vérifications de format de type YMDH, MDH, DH - le format H est géré à part.
        YMD = re.search(calendar.YMD_regex, datetime_str);
        T = re.search(calendar.time_regex, datetime_str);
        datetime_str = datetime_str.replace("T", "");
        lg_str = 0 ; # this allows to check there is no additional substrings.
        # Gestion de la date
        if YMD:
            now = datetime.now();
            year, month, day = now.year, now.month, now.day;
            date = YMD.group(0);
            lg_str += len(date);
            date_split = date.split("-");
            if len(date_split) == 3:
                type = event_type.YMDT;
                year, month, day = int(date_split[0]), int(date_split[1]), int(date_split[2])
            elif len(date_len) == 2:
                month, day = int(date_split[0]), int(date_split[1]);
                type = event_type.MDT;
            elif len(date_len) == 1:
                day = int(date_split);
                type = event_type.DT;
        # Gestion de l'heure
        if T:
            time = T.group(0);
            lg_str += len(time);
            time_split = time.split(":");
            hour, minute = int(time_split[0]), int(time_split[1]);
        else:
            hour, minute = 0, 0;
        try:
            datetime_obj = datetime(year, month, day, hour, minute);
            ret = calendar.datetime_type(type, datetime_obj);
        except:
            ret = event_type.ERROR;
        if (lg_str != len(datetime_str)):
            ret = event_type.ERROR;
        return ret;

    # [2018-5-2]&[ANNIV]&[Anniversaire de tbot]
    # @classmethod
    # def parse(cls, cmd):
    #     check_cmd = re.search(cls.date_regex, cmd)
    #     if re.search(cls.date_regex, cmd): # string is well formated.
    #         cmd_split = cmd.split('&');
    #         date = cmd_split ;
    #         cmd_split = cmd_split[1:-1]; # remove brackets
    #         try:
    #             datetime.fromisoformat()




if __name__ == "__main__":
    YMDT_str = "1961-03-30T19:43"
    a = calendar.parse_YMDT(YMDT_str);
    print(a)
