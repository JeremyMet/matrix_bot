from matrix_utils_room import matrix_utils_room ;
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.mastermind.mastermind_bot import mastermind_bot ;
from modules.greeting.greeting import greeting ;
from modules.admin.admin import admin ;
from modules.quotes.quotes import quotes ;
from modules.template.template import template ;
from modules.regex.regex import regex ;
from modules.loto.loto_bot import loto_bot;
from modules.url.url_bot import url_bot;
from modules.calendar.calendar_bot import calendar_bot;
import time ;


if __name__ == "__main__":


    # Instantiate modules
    my_pendu = pendu_bot("pendu", is_permanent = True) ;
    my_mastermind_0 = mastermind_bot("mastermind", is_permanent = True)
    my_mastermind_1 = mastermind_bot("mastermind", is_permanent = True)
    #my_greeting = greeting("greeting") ;
    #my_admin = admin("admin", is_permanent = True) ;
    my_quotes = quotes("quotes", hour=7, minute=0) ;
    my_loto = loto_bot("loto", hour=20, minute=30);
    my_url = url_bot();
    my_calendar_bot = calendar_bot() ;
    # Then Create the matrix object, add rooms, services and timers.
    matrix_obj = matrix_utils_room() ;

    admin_room = matrix_obj.add_room("#admin:mandragot.org", "Tbot, ready for action !")
    shared_admin_room = matrix_obj.add_room("#tbot_admin:mandragot.org", "Tbot, ready for action !")
    gaming_room = matrix_obj.add_room("#botgaming:mandragot.org", "Tbot, ready for action !")
    science_room = matrix_obj.add_room("#sciences:mandragot.org")
    music_room = matrix_obj.add_room("#musiciensdimanche:mandragot.org")
    main_room = matrix_obj.add_room("#deuxsurdix:mandragot.org")
    ludo_room = matrix_obj.add_room("#gaming:mandragot.org")

    matrix_obj.add_service_to_room(admin_room, my_mastermind_0) ;
    # matrix_obj.add_service_to_room(admin_room, my_calendar_bot);
    #
    matrix_obj.add_service_to_room(shared_admin_room, my_calendar_bot);
    #
    matrix_obj.add_service_to_room(main_room, my_calendar_bot);
    #
    matrix_obj.add_service_to_room(gaming_room, my_quotes) ;
    matrix_obj.add_service_to_room(gaming_room, my_pendu) ;
    matrix_obj.add_service_to_room(gaming_room, my_mastermind_1) ;
    matrix_obj.add_service_to_room(gaming_room, my_loto) ;
    matrix_obj.add_service_to_room(gaming_room, my_calendar_bot);
    # #
    matrix_obj.add_service_to_room(gaming_room, my_url) ;
    matrix_obj.add_service_to_room(science_room, my_url) ;
    matrix_obj.add_service_to_room(music_room, my_url) ;
    matrix_obj.add_service_to_room(main_room, my_url) ;
    matrix_obj.add_service_to_room(ludo_room, my_url) ;

    matrix_obj.start_timer() ; # start clock thread (for clock sensitive processes/modules)
    matrix_obj.spawn() ;
