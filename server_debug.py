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
from modules.echo.echo_bot import echo_bot;
import time ;


if __name__ == "__main__":


    # Instantiate modules
    my_pendu = pendu_bot("pendu", is_permanent = True) ;
    my_echo = echo_bot();
    # Then Create the matrix object, add rooms, services and timers.
    matrix_obj = matrix_utils_room() ;

    debug_room = matrix_obj.add_room("#toto-gaming:mandragot.org", "Tbot, ready for action !")
    gaming_room = matrix_obj.add_room("#botgaming:mandragot.org", "Tbot, ready for action !")


    matrix_obj.add_service_to_room(debug_room, my_pendu) ;
    matrix_obj.add_service_to_room(debug_room, my_echo) ;
    matrix_obj.add_service_to_room(gaming_room, my_echo) ;



    matrix_obj.start_timer() ; # start clock thread (for clock sensitive processes/modules)
    matrix_obj.spawn() ;
