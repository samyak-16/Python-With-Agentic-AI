# def greet(name):  # layer 1 — receives "Samyak"
#     def decorator(func):  # layer 2 — receives the function
#         def wrapper():  # layer 3 — runs when called
#             print(f"Hello {name}!")
#             func()

#         return wrapper

#     return decorator


# @greet(name="Samyak")  # now greet receives "Samyak" FIRST, not the function
# def my_func():
#     print("I am the function")


# my_func()
# # Hello Samyak!
# # I am the function


# Manual Form------------------------------------------------------------------------


def greet(name):  # layer 1 — receives "Samyak"
    def decorator(func):  # layer 2 — receives the function
        def wrapper():  # layer 3 — runs when called
            print(f"Hello {name}!")
            func()

        return wrapper

    return decorator


def my_func():
    print("I am the function")


step1 = greet("samyak")
step2 = step1(my_func)
step2()

# Closure helps to same "name" temperorarily in memory linking with the fun itself
