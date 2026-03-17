# def local_chai():
#     yield "Masala Chai"
#     yield "Ginger Chai"


# def imported_chai():
#     yield "Matcha"
#     yield "Oolang"

# def full_menue():
#     yield from local_chai()
#     yield from imported_chai()
 
# menue = full_menue()

# print(next(menue))
# print(next(menue))
# print(next(menue))
# print(next(menue))


def chai_stall():
    try:
        while True:
             yield "Waiting for chai order"
             yield "Waiting for second chai order"
    except:

        print("Stall closed , No more close ")

stall =  chai_stall()

print(next(stall))
print("Hello world test")
stall.close() # --> Throws GeneratorExit Exception -- cleaning up your memory
print(next(stall)) # Wont work cause generator alr closed 

# so if we have two yield in a generator and we only called next once and program ends then also the except block is triggered ? at the last of the program .
