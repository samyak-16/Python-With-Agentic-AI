class InvalidChaiError(Exception):
    pass


def bill(flavour, cups):
    menu = {"masala": 20, "ginger": 40}
    try:
        if flavour not in menu:
            raise InvalidChaiError("That chai isn't available")
        if not isinstance(cups, int):
            raise TypeError("Number of cups must be an interger")
        total = menu[flavour] * cups
        print(f"Your bill for {cups} cups of {flavour} chai is Rs.{total}")
    except Exception as e:
        print("Error :", e)
    finally:
        print("Thankyou for learning to handle error in python :)")


bill("mint",2)
bill("masala","three")
bill("ginger","three")
bill("masala",10)