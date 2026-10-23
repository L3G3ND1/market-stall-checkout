
import time
from functools import wraps

logged_in = False


def total_prices(*prices):
    return sum(prices)


def add_to_cart(cart, *items):
    cart.extend(items)
    return cart


def receipt(*items, discount=0):
    subtotal = total_prices(*(price for name, price in items))

    print("\n========== MARKET STALL RECEIPT ==========")

    for name, price in items:
        print(f"{name:<20} ₦{price:,.2f}")

    print("------------------------------------------")
    print(f"{'Subtotal:':<20} ₦{subtotal:,.2f}")
    print(f"{'Discount:':<20} ₦{discount:,.2f}")
    print(f"{'Final Total:':<20} ₦{subtotal - discount:,.2f}")
    print("==========================================")


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
            print("Access denied: please log in as cashier.")
            return None

        return func(*args, **kwargs)

    return wrapper


def no_negative_prices(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        values = list(args) + list(kwargs.values())

        for value in values:
            if isinstance(value, (int, float)) and value < 0:
                print("Rejected: prices cannot be negative.")
                return None

            if isinstance(value, (tuple, list)):
                for part in value:
                    if isinstance(part, (int, float)) and part < 0:
                        print("Rejected: prices cannot be negative.")
                        return None

        return func(*args, **kwargs)

    return wrapper


@no_negative_prices
def calculate_total(*prices):
    return total_prices(*prices)


@no_negative_prices
@require_cashier
def complete_sale(*items):
    receipt(*items)


@timer
@log_call
def sample_operation(amount, multiplier=2):
    time.sleep(0.1)
    return amount * multiplier


def run_tests():
    global logged_in

    print("\n--- TEST 1: LOGGING ---")
    result = sample_operation(5, multiplier=3)
    print("Result:", result)

    print("\n--- TEST 2: NEGATIVE PRICE ---")
    print("Valid total:", calculate_total(500, 1200, 300))
    print("Invalid total:", calculate_total(500, -200, 300))

    print("\n--- TEST 3: CASHIER LOGIN ---")
    items = (("Yam", 1500), ("Rice", 2500))

    complete_sale(*items)

    logged_in = True
    print("Cashier logged in.")

    complete_sale(*items)

    print("\n--- TEST 4: NEGATIVE ITEM PRICE ---")
    complete_sale(("Yam", -1500))


if __name__ == "__main__":
    run_tests()
