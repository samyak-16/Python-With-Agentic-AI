# Generators in Python  : yield as a keyword , 

# Most important part of generators :
# we save memory 
# we dont want results immedietly 
# lazy object : evalutations 


# def server_chai():
#     yield "Cup 1 : Masala Chai" 
#     yield "Cup 2 : Normal Chai" 
#     yield "Cup 3 : Stall Chai" 
#     yield "Cup 4 : Sam Chai" 

# stall = server_chai()
# print(list(stall))


# normal - computes ALL values, stores in memory

def get_numbers(n):
    result = []
    for i in range(n):
        result.append(i*2)
    return result

print(get_numbers(5))

# generator - produces ONE value at a time 

def gen_numbers(n):
    for i in range(n):
        yield i*2

gen = gen_numbers(5)
print(next(gen))  # 0
print(next(gen))  # 2
print(next(gen))  # 4