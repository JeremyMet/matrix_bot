from matrix_utils import matrix_utils ;
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.greeting.greeting import greeting ;
from modules.admin.admin import admin ;




if __name__ == "__main__":

    # Instantiate modules
    my_pendu = pendu_bot() ;
    my_pendu.set_clock_sensitive_off() ;
    my_greeting = greeting() ;
    my_admin = admin() ;
    # Then Create the matrix object, add rooms, services and timers.
    matrix_obj = matrix_utils() ;
    gaming_room = matrix_obj.add_room("#toto-gaming:mandragot.org")
    # gaming_room = matrix_obj.add_room("#deuxsurdix-gaming:bobbyblues.com")
    main_room = matrix_obj.add_room("#deuxsurdix:mandragot.org")
    # Add timer to rooms
    matrix_obj.add_timer_to_room(gaming_room)
    matrix_obj.add_timer_to_room(main_room)
    # Add services :)
    matrix_obj.add_service_to_room(main_room, "greeting", my_greeting)
    matrix_obj.add_service_to_room(main_room, "admin", my_admin)
    matrix_obj.add_service_to_room(main_room, "pendu", my_pendu)


    matrix_obj.add_service_to_room(gaming_room, "pendu", my_pendu) ;
    matrix_obj.add_service_to_room(gaming_room, "greeting", my_greeting) ;
    matrix_obj.add_service_to_room(gaming_room, "admin", my_admin) ;
    # my_greeting.set_module_off() ;
    # Start timer
    matrix_obj.start_timer()
    # And run
    matrix_obj.remove_timer_from_room(main_room)
    # matrix_obj.remove_room(main_room)
    matrix_obj.spawn() ;