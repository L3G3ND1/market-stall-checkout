
from functools import wraps
commands = {}
cart = []
logged_in = False


def command(func):
    commands[func.__name__] = func
    return func



def require_cashier(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in:
            print("Access denied. Please log in first.")
            return
        return func(*args, **kwargs)

    return wrapper



@command
def login():
    global logged_in
    logged_in = True
    print("Cashier logged in successfully.")


@command
@require_cashier
def add_item():
    name = input("Item name: ").strip()

    try:
        price = float(input("Item price: "))
        if price < 0:
            print("Price cannot be negative.")
            return
    except ValueError:
        print("Enter a valid numeric price.")
        return

    cart.append((name, price))
    print(f"{name} added to cart.")


@command
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

        if cmd not in commands:
            print(f"Unknown command: {cmd}")
            continue

        commands[cmd]()


if __name__ == "__main__":
    main()
