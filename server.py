from matrix_utils import matrix_utils ;
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.greeting.greeting import greeting ;



if __name__ == "__main__":

    # Instantiate modules
    my_pendu = pendu_bot() ;
    my_greeting = greeting() ;
    # Then Create the matrix object, add rooms and services.
    matrix_obj = matrix_utils() ;
    # gaming_room = matrix_obj.add_room("#toto-gaming:mandragot.org")
    gaming_room = matrix_obj.add_room("#deuxsurdix-gaming:bobbyblues.com")
    main_room = matrix_obj.add_room("#toto:mandragot.org")
    matrix_obj.add_service_to_room(gaming_room, "pendu", my_pendu) ;
    # Add timer to rooms
    matrix_obj.add_timer_to_room(gaming_room)
    matrix_obj.add_timer_to_room(main_room)
    matrix_obj.add_service_to_room(main_room, "greeting", my_greeting)
    # Start timer
    matrix_obj.start_timer()
    # And run
    matrix_obj.spawn() ;