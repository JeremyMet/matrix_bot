from matrix_utils import matrix_utils ;
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.greeting.greeting import greeting ;
from modules.admin.admin import admin ;
from modules.quotes.quotes import quotes ;
from modules.template.template import template ;
# import logging

# It would have been more clever to distinguish passive services from active ones ;
# It would have removed "heavy" loop" (use of dictionaries instead for service call).
# But well ... ;-)



if __name__ == "__main__":


    # Instantiate modules
    my_pendu = pendu_bot("pendu", is_permanent = True) ;
    # my_pendu.set_clock_sensitivity_on() ;
    my_greeting = greeting("greeting") ;
    my_admin_0 = admin("admin", is_permanent = True) ;
    my_admin_1 = admin("admin", is_permanent = True);
    my_quotes = quotes("quotes") ;
    my_template = template()
    # Then Create the matrix object, add rooms, services and timers.
    matrix_obj = matrix_utils() ;
    gaming_room = matrix_obj.add_room("#toto-gaming:mandragot.org")
    # gaming_room = matrix_obj.add_room("#deuxsurdix-gaming:bobbyblues.com")
    main_room = matrix_obj.add_room("#toto:mandragot.org")
    # admin_room = matrix_obj.add_room("#admin:mandragot.org")
    # Add timer to services
    # Add services :)

    matrix_obj.add_service_to_room(main_room, my_greeting)
    matrix_obj.add_service_to_room(main_room , my_quotes) ,
    matrix_obj.add_service_to_room(main_room, my_template)

    matrix_obj.add_service_to_room(gaming_room, my_pendu) ;
    matrix_obj.add_service_to_room(gaming_room, my_greeting);

    # matrix_obj.add_service_to_room(admin_room, my_admin_0, "tbot admin install_from_list \
    #  https://gist.githubusercontent.com/JeremyMet/1581ec044d487302d2f2f60911e5f02a/raw/cbbc5d4149abafb7a653f2e1e88825a55f1ec90f/module_list.txt");
    matrix_obj.add_service_to_room(main_room, my_admin_1) ;

    # my_greeting.set_module_off() ;
    # Start timer
    matrix_obj.add_timer_to_service(my_quotes);
    matrix_obj.add_timer_to_service(my_pendu);
    # matrix_obj.add_timer_to_service(my_admin_0);
    matrix_obj.add_timer_to_service(my_admin_1);
    matrix_obj.start_timer()
    # And run
    matrix_obj.spawn() ;