# def brew_chai(flavour):
#     if flavour not in ["Masala", "Ginger", "elachei"]:
#         raise ValueError("Unsupported Chai")
#     print(f"brewing {flavour} chai..")


# # brew_chai("mint")

class OutOfIngridientsError(Exception):
    pass

def make_chai(milk,sugar):
    if(milk == 0 or sugar==0) :
        raise OutOfIngridientsError("Missing milk or sugar")
    print ("Chai is ready")

make_chai(0,0)