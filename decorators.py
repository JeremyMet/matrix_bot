import threading;


def lock_dec(function):
    lock = threading.Lock();
    def wrapper(*args, **kargs):
        with lock:
            return function(*args, **kargs) ;
    return wrapper ;
