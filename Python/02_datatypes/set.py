essential_spices = {"xard","ginger","optional_spices"}
optional_spices = {"cloves","ginger","blackpeper",}
all_spices = essential_spices | optional_spices
print(all_spices)

common_spices  = essential_spices & optional_spices
print(common_spices)

only_in_essential = essential_spices - optional_spices 
print(only_in_essential)