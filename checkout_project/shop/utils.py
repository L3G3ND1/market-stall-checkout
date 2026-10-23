
def total_prices(*prices):
    return sum(prices)


def add_to_cart(cart, *items):
    cart.extend(items)
    return cart


def receipt(*items, discount=0, cashier_id="", phone=""):
    subtotal = total_prices(*(price for name, price in items))

    print("\n========== MARKET RECEIPT ==========")

    if cashier_id:
        print(f"Cashier: {cashier_id}")

    if phone:
        print(f"Customer phone: {phone}")

    for name, price in items:
        print(f"{name:<20} ₦{price:,.2f}")

    print("------------------------------------")
    print(f"{'Subtotal:':<20} ₦{subtotal:,.2f}")
    print(f"{'Discount:':<20} ₦{discount:,.2f}")
    print(f"{'Final Total:':<20} ₦{subtotal - discount:,.2f}")
    print("====================================")

    return subtotal - discount
