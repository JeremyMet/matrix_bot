from matrix_utils_ext import matrix_utils_ext ;
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.mastermind.mastermind_bot import mastermind_bot ;
from modules.greeting.greeting import greeting ;
from modules.admin.admin import admin ;
from modules.quotes.quotes import quotes ;
from modules.template.template import template ;
from modules.regex.regex import regex ;
from modules.loto.loto_bot import loto_bot;
import time ;


if __name__ == "__main__":


    # Instantiate modules
    my_pendu = pendu_bot("pendu", is_permanent = True) ;
    my_mastermind = mastermind_bot("mastermind", is_permanent = True)
    #my_greeting = greeting("greeting") ;
    #my_admin = admin("admin", is_permanent = True) ;
    my_quotes = quotes("quotes", hour=23, minute=0) ;
    my_loto = loto_bot("loto", hour=20, minute=30);
    # Then Create the matrix object, add rooms, services and timers.
    matrix_obj = matrix_utils_ext() ;
    gaming_room = matrix_obj.add_room("#botgaming:mandragot.org")
    # gaming_room = matrix_obj.add_room("#admin:mandragot.org")

    matrix_obj.add_service_to_room(gaming_room, my_quotes) ;
    matrix_obj.add_service_to_room(gaming_room, my_pendu) ;
    matrix_obj.add_service_to_room(gaming_room, my_mastermind) ;
    matrix_obj.add_service_to_room(gaming_room, my_loto) ;

    matrix_obj.start_timer() ; # start clock thread (for clock sensitive processes/modules)
    matrix_obj.spawn() ;
