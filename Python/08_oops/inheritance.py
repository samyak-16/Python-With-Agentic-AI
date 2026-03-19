class BaseChai :
    def __init__(self,type_):
        self.type = type_

    def prepare(self):
        print(f"Preparing {self.type} chai.....")

class MasalaChai(BaseChai):
    def add_spices(self):
        print("Adding cardamon , ginger , cloves")

class ChaiShop:
    chai_class = BaseChai # Composition / Factory pattern 
    
    def __init__(self):
        self.chai = self.chai_class("Regular")
        print(self.chai_class("Regular"))
    
    def serve(self):
        print(f"Serving {self.chai.type} chain in the shop")
        self.chai.prepare()

class FancyChaiShop(ChaiShop):
    chai_class = MasalaChai

shop = ChaiShop()
fancy = FancyChaiShop()
shop.serve()
fancy.serve()



