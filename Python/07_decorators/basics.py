# def my_decorator(func):
#     def wrapper():
#         print("Before function runs")
#         func()
#         print("After function runs")
#     return wrapper 

# def greet():
#     print(f"Hello , sir/mam")

# greet = my_decorator(greet) # wraps it manually 
# greet()

# Before function runs
# Hello , sir/mam
# After function runs

from functools import wraps
# wraps preservs the metadata of the wrapped function like fn.__name__ etc...
def my_decorator(func):
    @wraps(func) # using this preservs the meta data of the function 
    def wrapper():
        print("Before function runs")
        func()
        print("After function runs")
    return wrapper 

@my_decorator # syntatical sugar : same as greet = my_decorator(greet) 
def greet():
    print(f"Hello , sir/mam")

greet()
print(greet.__name__)

# Before function runs
# Hello , sir/mam
# After function runs