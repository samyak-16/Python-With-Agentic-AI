class Chai :
    origin = "India" # Properties 

print(Chai.origin) # India
Chai.is_hot = True #Declaring properties for the class Chai
print(Chai.is_hot) # True



#  Creating objects from class Chai

masala = Chai()

print(f"masala {masala.origin}")
print(f"masala {masala.is_hot}")

masala.is_hot = False

print(f" chai {Chai.is_hot}")
print(f"masala {masala.is_hot}")
