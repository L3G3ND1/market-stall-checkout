
from shop import (
    commands,
    command,
    no_negative_prices,
    require_cashier,
    set_logged_in,
    validate_cashier_id,
    validate_phone,
    CMD,
    receipt,
)
from shop.utils import add_to_cart
from shop.exceptions import NotLoggedInError

cart = []
cashier_id = ""


@command
def login():
    global cashier_id

    entered_id = input("Cashier ID (CSH-0000): ").strip()
    validate_cashier_id(entered_id)

    cashier_id = entered_id
    set_logged_in(True)
    print(f"Welcome, cashier {cashier_id}.")


@command
@no_negative_prices
@require_cashier
def add(item, price):
    add_to_cart(cart, (item.title(), price))
    print(f"{item.title()} added for ₦{price:,.2f}.")


@command
@require_cashier
def show_receipt():
    if not cart:
        print("Your cart is empty.")
        return

    phone = input("Customer phone number: ").strip()
    validate_phone(phone)
    receipt(*cart, cashier_id=cashier_id, phone=phone)


@command
def logout():
    global cashier_id
    set_logged_in(False)
    cashier_id = ""
    print("Cashier logged out.")


@command
def help():
    print("\nAvailable commands:")
    print("login")
    print("add Yam 1500")
    print("show_receipt")
    print("logout")
    print("help")
    print("quit")


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
                        "Use this format: add Yam 1500"
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

        except NotLoggedInError as e:
            print(e)
        except ValueError as e:
            print(f"Invalid input: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nCheckout closed.")
            break


if __name__ == "__main__":
    main()
