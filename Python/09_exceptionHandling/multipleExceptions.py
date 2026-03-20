def process_order(item, quantity):
    try:
        price = {"Masala": 20}[item]
        cost = price * quantity
        print(f"total cost is{cost}")

    except KeyError:
        print("Sorry that chai is not on menue")

    except TypeError:
        print("Quantity must be in number")

process_order("ginger",2)
process_order("Masala","two")
