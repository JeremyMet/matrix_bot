# Matrix OS

Matrix OS is a simple Python program that facilitates service deployment across Matrix Rooms.
Services (or modules) are Python scripts which process room sent messages. For instance, a message can ask a given module *A* to print out the current weather. Module *A* will then interpret the order, will "understand" its meaning and return the desired information. Matrix OS is mainly a small framework to "chat bot".

## Who does it work ?

The following snippet gives a quicj overview of Matrix_OS functionnalities:

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
First, one instantiates modules. The modules should follow a specific structure (that you may find in the modules/template folder). Each module is composed of (at least) three methods, one (*run*) that will be in charged of "message processing", one (*run_on_clock*) that will be activated every second (that you may use to display weather every hour of the day) and one (*exit*) that will be called when the service is shut down (this can be useful to save temporary variables into files).

Then, the matrix object is created. It will load login information (server/login/password) from *config.json* file.
One can finally add rooms and services before running matrix_os bot (*matrix_obj.spawn()*).

Note that each room "lives" independently in a sense that each room does have its service list. Services can be shared between room. All services are "clock sensitive" by default (meaning their *run_on_clock* subroutines will be called once per second). This sensitiviy removed however (*module.set_clock_sensitivity_off()*).
