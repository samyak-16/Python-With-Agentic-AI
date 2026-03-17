def make_chai(tea,milk,sugar):
    print(f"Tea : {tea} , milk : {milk} , sugar : {sugar}")
make_chai("Darjeeling","Yes", "Low") # Positional args
make_chai("Darjeeling",sugar="No",milk="Yes") # keywords 

def special_chai(*ingridents , **extras):
     print(f"Ingredients" , ingridents)
     print(f"Extras",extras)

special_chai("Cinnamon","Cardmom", sweetner="Honey")