from time import time
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    filename='debug.log',
                    filemode='w',
                    level=logging.DEBUG)
                    # level=logging.INFO)


# while we can use @profiler.time_function annotation, lets separate out debugging in this custom annotation
def timeit(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logging.debug(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        # print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func
