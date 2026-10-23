
import time
from functools import wraps
from .exceptions import NotLoggedInError

commands = {}
logged_in = False


def command(func):
    commands[func.__name__] = func
    return func


def set_logged_in(value):
    global logged_in
    logged_in = value


def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        print(f"Arguments: args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f} seconds")
        return result
    return wrapper


def require_cashier(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in:
            raise NotLoggedInError(
                "Access denied. Please log in as cashier first."
            )
        return func(*args, **kwargs)
    return wrapper


def no_negative_prices(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def check(value):
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("Prices cannot be negative.")

            if isinstance(value, (tuple, list)):
                for part in value:
                    check(part)

        for value in args:
            check(value)

        for value in kwargs.values():
            check(value)

        return func(*args, **kwargs)
    return wrapper


def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator
