def print_name(name):
    '''This function prints the name given by the user itself with some added string on it '''
    print(f"your name is {name}")

print(print_name.__doc__)
print(print_name.__name__)

help(print)