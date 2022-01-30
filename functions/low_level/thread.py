import threading


def thread(func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        my_thread.start()

    return wrapper


def none_died_thread(func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(
            target=func, args=args, kwargs=kwargs, daemon=False
        )
        my_thread.start()

    return wrapper
