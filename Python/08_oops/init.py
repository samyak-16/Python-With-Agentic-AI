class ChaiORder:
    def __init__(self,type_,size): # Runs everytime when we create object (instance) from a class 
        self.type = type_
        self.size = size

    def add_price(self,price):
        self.price = price 
    
    def summary(self):
        return f"{self.size}ml of {self.type} chai"

c1 = ChaiORder("Big","XL")

c1.add_price(100) 

print(c1.price)
print(c1.type)