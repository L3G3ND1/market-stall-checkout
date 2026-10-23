
import re
from functools import wraps

commands = {}
cart = []
logged_in = False
cashier_id = ""

CMD = re.compile(
    r"^add\s+(?P<item>[A-Za-z]+)\s+(?P<price>\d+)$",
    re.IGNORECASE
)

CASHIER_PATTERN = re.compile(r"^CSH-\d{4}$")
PHONE_PATTERN = re.compile(
    r"^(?:0[789][01]\d{8}|\+?234[789][01]\d{8})$"
)


class NotLoggedInError(Exception):
    pass


def validate_cashier_id(value):
    if not CASHIER_PATTERN.fullmatch(value):
        raise ValueError("Cashier ID must follow CSH-0000 format.")
    return value


def validate_phone(value):
    if not PHONE_PATTERN.fullmatch(value):
        raise ValueError(
            "Enter a valid Nigerian phone number, e.g. 08012345678."
        )
    return value


def command(func):
    commands[func.__name__] = func
    return func


def no_negative_prices(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for value in list(args) + list(kwargs.values()):
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
    global logged_in, cashier_id

    entered_id = input("Enter cashier ID (CSH-0000): ").strip()
    validate_cashier_id(entered_id)

    cashier_id = entered_id
    logged_in = True
    print(f"Welcome, cashier {cashier_id}.")


@command
@no_negative_prices
@require_cashier
def add(item, price):
    if not item.isalpha():
        raise ValueError("Item name must contain letters only.")

    cart.append((item.title(), price))
    print(f"{item.title()} added for ₦{price:,.2f}.")


@command
@require_cashier
def show_receipt():
    if not cart:
        print("Your cart is empty.")
        return

    phone = input("Customer phone number: ").strip()
    validate_phone(phone)

    subtotal = sum(price for name, price in cart)

    print("\n========== MARKET RECEIPT ==========")
    print(f"Cashier: {cashier_id}")
    print(f"Customer phone: {phone}")

    for name, price in cart:
        print(f"{name:<20} ₦{price:,.2f}")

    print("------------------------------------")
    print(f"{'Total:':<20} ₦{subtotal:,.2f}")
    print("====================================")


@command
def help():
    print("\nAvailable commands:")
    print("login                 - Log in as cashier")
    print("add Yam 1500           - Add an item and its price")
    print("show_receipt           - Print the receipt")
    print("logout                 - Log out")
    print("help                   - Show available commands")
    print("quit                   - Exit checkout")


@command
def logout():
    global logged_in, cashier_id
    logged_in = False
    cashier_id = ""
    print("Cashier logged out.")


def main():
    print("Welcome to Market Stall Checkout!")
    print("Type help to see available commands.")

    while True:
        try:
            user_input = input("\nCommand: ").strip()

            if user_input.lower() == "quit":
                print("Checkout closed.")
                break

            if user_input.lower().startswith("add "):
                match = CMD.fullmatch(user_input)

                if not match:
                    raise ValueError(
                        "Invalid add command. Use: add Yam 1500 "
                        "with a non-negative whole-number price."
                    )

                item = match.group("item")
                price = int(match.group("price"))
                commands["add"](item, price)
                continue

            cmd = user_input.lower()
            if cmd not in commands:
                print(f"Unknown command: {user_input}")
                continue

            commands[cmd]()

        except KeyError:
            print(f"Unknown command: {user_input}")
        except NotLoggedInError as e:
            print(e)
        except ValueError as e:
            print(f"Invalid input: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nCheckout closed.")
            break


if __name__ == "__main__":
    main()
