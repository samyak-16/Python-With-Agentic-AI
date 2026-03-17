from functools import wraps

def required_admin(func):
    @wraps(func)
    def wrapper(user_role):
        if user_role != "admin" :
            print("Access denied : Admins Only")
        else:
            return func(user_role)
    return wrapper


# Manual wrapping :
# def access_tea_inventory(role):
#     print("Access granted to the inventory")

# access_tea_inventory = required_admin(access_tea_inventory)

# access_tea_inventory("admin")
# access_tea_inventory("user")

# syntatical sugar wrapping wsing @
@required_admin
def access_tea_inventory(role):
    print("Access granted to the inventory")

access_tea_inventory("admin")
access_tea_inventory("user")
