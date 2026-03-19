# Multiple Inheritance and MRO - Method Resolution Order

class A :
    lable = "A: Base class"
    pass
class B(A) :
    lable = "B: Masala blend"
    pass
class C(A) :
    lable = "C: Herbal blend"
    pass
class D(B,C) :
    pass
class E(C,B) :
    pass


cup = D()
cup1 = E()

print(cup.lable) # B: Masala blend
print(cup1.lable) # C: Masala blend

print("MRO information :" , D.__mro__)
