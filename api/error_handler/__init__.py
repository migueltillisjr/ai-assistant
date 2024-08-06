from log import *
import traceback

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            logging.info(f'*** Running {func} ** Data -> {args} {kwargs}')
            return func(*args, *kwargs)
        except Exception as e:
            trace = traceback.format_exc()
            print(trace)
            print(f'An error occured: {e}')
            logging.error(f'*** Error {e} *** {trace}')
    return wrapper