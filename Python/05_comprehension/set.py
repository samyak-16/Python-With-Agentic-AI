# mixed_numbers = [ 1,2,3,1,1,2,2,4,4,44,45,42,11,1,2,3,4,5,6,7,8,9,10]


# unique_value  = {number for number in mixed_numbers}
# print(unique_value)
# print(sorted(unique_value))




recipies = {
    "Masala Chai" : ["ginger", "cardamon","clove"],
    "Elaichi Chai" : ["cardamon", "milk"],
    "Spicy Chai" : ["ginger", "black pepper","clove"],
}

# Find unique spicies 


# nested loop → nested comprehension
# [what_to_collect   for outer_loop   for inner_loop]


unique_spices = {spices for ingridents in recipies.values() for spices in ingridents}

# print(recipies.values())
print (unique_spices)