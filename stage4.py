
from functools import wraps

commands = {}
cart = []
logged_in = False


class NotLoggedInError(Exception):
    pass


def command(func):
    commands[func.__name__] = func
    return func


def no_negative_prices(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        values = list(args) + list(kwargs.values())

        for value in values:
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("Prices cannot be negative.")

            if isinstance(value, (tuple, list)):
                for part in value:
                    if isinstance(part, (int, float)) and part < 0:
                        raise ValueError("Prices cannot be negative.")

        return func(*args, **kwargs)

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


@command
def login():
    global logged_in
    logged_in = True
    print("Cashier logged in successfully.")


@command
@no_negative_prices
@require_cashier
def add_item():
    name = input("Item name: ").strip()

    if not name:
        raise ValueError("Item name cannot be empty.")

    price = float(input("Item price: "))

    if price < 0:
        raise ValueError("Prices cannot be negative.")

    cart.append((name, price))
    print(f"{name} added to cart.")


@command
@no_negative_prices
@require_cashier
def show_receipt():
    if not cart:
        print("Your cart is empty.")
        return

    subtotal = sum(price for name, price in cart)

    print("\n========== MARKET RECEIPT ==========")

    for name, price in cart:
        print(f"{name:<20} ₦{price:,.2f}")

    print("------------------------------------")
    print(f"{'Total:':<20} ₦{subtotal:,.2f}")
    print("====================================")


@command
def help():
    print("Available commands:")
    for name in commands:
        print(f"- {name}")
    print("- quit")


@command
def logout():
    global logged_in
    logged_in = False
    print("Cashier logged out.")


def main():
    print("Welcome to Market Stall Checkout!")
    print("Type help to see available commands.")

    while True:
        cmd = input("\nCommand: ").strip().lower()

        if cmd == "quit":
            print("Checkout closed.")
            break

        try:
            commands[cmd]()
        except KeyError:
            print(f"Unknown command: {cmd}")
        except NotLoggedInError as e:
            print(e)
        except ValueError as e:
            print(f"Invalid input: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nCheckout closed.")
            break


if __name__ == "__main__":
    main()
