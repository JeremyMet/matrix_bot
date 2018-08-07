from matrix_utils import matrix_utils ;
from modules.pendu_bot.pendu_bot import pendu_bot ;
from modules.greeting.greeting import greeting ;



if __name__ == "__main__":

    matrix_obj = matrix_utils() ;
    my_pendu = pendu_bot() ;
    my_greeting = greeting() ;
    gaming_room = matrix_obj.add_room("#toto-gaming:mandragot.org")
    # gaming_room = matrix_obj.add_room("#deuxsurdix-gaming:bobbyblues.com")
    main_room = matrix_obj.add_room("#toto:mandragot.org")
    matrix_obj.add_service_to_room(gaming_room, "pendu", my_pendu) ;
    matrix_obj.add_timer(gaming_room, 2)
    matrix_obj.add_service_to_room(main_room, "greeting", my_greeting)
    matrix_obj.spawn() ;