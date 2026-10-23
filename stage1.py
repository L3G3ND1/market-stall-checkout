
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

    final_total = subtotal - discount
    print(f"{'Final Total:':<20} ₦{final_total:,.2f}")
    print("==========================================")

    return final_total


if __name__ == "__main__":
    cart = []

    add_to_cart(
        cart,
        ("Yam", 1500),
        ("Rice", 2500),
        ("Beans", 1200)
    )

    print("Total prices:", total_prices(500, 1200, 300))

    receipt(*cart, discount=200)
