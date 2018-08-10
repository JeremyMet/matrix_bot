# Matrix OS

Matrix OS is a simple Python program that facilitates service deployment across Matrix Rooms.
Services (or modules) are Python scripts which process room sent messages. For instance, a message can ask a given module *A* to print out the current weather. Module *A* will then interpret the order, will "understand" its meaning and return the desired information. Matrix OS is mainly a small framework to "chat bot".

## Who does it work ?

The following snippet gives an overview of Matrix_OS functionnalities 

```pyton

    # Instantiate modules (services)
    my_pendu = pendu_bot() ;
    my_greeting = greeting() ;
    my_admin = admin() ;
    my_quotes = quotes() ;
    
    # Then Create the matrix object, add rooms, services and timers.
    matrix_obj = matrix_utils() ;
    gaming_room = matrix_obj.add_room("#toto-gaming:pouet.org")
    main_room = matrix_obj.add_room("#toto:pouet.org")
    
    # Add services :)
    matrix_obj.add_service_to_room(main_room, "greeting", my_greeting)
    matrix_obj.add_service_to_room(main_room, "admin", my_admin)
    matrix_obj.add_service_to_room(main_room, "quotes", my_quotes) ,

    matrix_obj.add_service_to_room(gaming_room, "pendu", my_pendu) ;
    matrix_obj.add_service_to_room(gaming_room, "greeting", my_greeting) ;
    matrix_obj.add_service_to_room(gaming_room, "admin", my_admin) ;
    # Start timer
    matrix_obj.start_timer()
    # Remove clock sensitivity for the my_greeting instantiation
    my_greeting.set_clock_sensitivity_off() ;
    # And run
    matrix_obj.spawn() ;
 ```
