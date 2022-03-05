import time


def timed(func):
    """
    records approximate durations of function calls
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"\n-----{func.__name__} started-----")
        result = func(*args, **kwargs)
        print(
            f"\n-----{func.__name__} finished in {time.time() - start:.2f} seconds-----"
        )
        return result

    return wrapper
