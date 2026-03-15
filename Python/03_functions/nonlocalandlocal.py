# global and nonlocal

def update_order():
    chai_type = "Elichi"
    def kitchen():  
        # chai_type = "kesar" # defined only for kitchen fn 
        nonlocal chai_type # just looks above the outer fn 
        chai_type = "Kesar"
        
    kitchen()
    print(chai_type)

update_order()

chai_type1 = "plain"
def frontDesk():
    def kitchen():
        global chai_type1
        chai_type1 = "Irani"

    kitchen()
frontDesk()
print(chai_type1)
