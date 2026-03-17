# Building a logger with python 
from functools import wraps


def log_activity(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        print(f"Calling : {func.__name__}")
        result = func(*args,**kwargs)
        print(f"Finished : {func.__name__}")
        return result 
    return wrapper

@log_activity
def add(num1,num2):
    print(   

    num1 + num2

    ) 

add(5,10)