# Matrix OS

Matrix OS is a simple Python program that facilitates service deployment across Matrix Rooms.
Services (or modules) are Python scripts which process room sent messages. For instance, a message can ask a given module *A* to print out the current weather. Module *A* will then interpret the order and return the desired information. Matrix OS is mainly a small framework for "chat bot".

## How does it work ?

The following snippet gives a quick overview of Matrix_OS functionnalities:

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

Internal clock (that ticks every second) should be run in case you have modules that may be clock sensitive. To do so, just type the *matrix_obj.start_timer()* instruction. The ticks can be stopped thanks to the *matrix_obj.stop_timer()* command.

Note that each room "lives" independently in a sense that each room does have its service list. Services can be shared between room. All services are "clock sensitive" by default (meaning their *run_on_clock* subroutines will be called once per second). This sensitiviy can be removed however (*module.set_clock_sensitivity_off()*). Plus, modules are activated when created, but it is possible to deactivate them (*module.set_module_off()*). It does not mean they are "desinstalled", it does mean that are in "sleep" mode and can be reactived any time soon (*module.set_module_on()*).

In a matrix room in which module *A* has been installed, one simply has to write *tbot A* to call the *A* module.
Of course, parameters can be added to the message as *tbot A parameter_0 paramater_1 ... parameter_n* but this input should be manually processed in the *run* method. 

Of course, it may be sometimes required to process a message that does not begin with "tbot". This can be handle by removing the  @module.check_command_dec decorator from the *run* method.

## Admin module

This module is a powerful one. It should not be instantiated in sensitive rooms as this module allows to install/desinstall/activate/deactivate modules.  

To install a new module from url, type the following
```
tbot admin install template https://gist.githubusercontent.com/JeremyMet/4016c881ae7b7e988fec542a4a04e470/raw/8faafe527e69cce48bbf1c9fc2e4b624b1bee5bc/template.py
```

To list all rooms:
```
tbot admin room_list
```

To list all services in a room:
```
tbot admin service_list
```

To activate a module:
```
tbot admin service_on __MODULE_NAME__
```

To deactivate a module:
```
tbot admin service_off __MODULE_NAME__
```

## Pendu module


