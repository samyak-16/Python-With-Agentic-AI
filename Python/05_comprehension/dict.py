# Dict comphrension 
tea_prices_inr = {
    "Masala Chai" : 40 , 
    "Green Chai" : 50 , 
    "Lemon Chai" : 200 , 
}

# Convert the prices into nepali using dict comphrension
# 
tea_prices_npr = {key:value*1.6 for key,value in tea_prices_inr.items()}
# print(tea_prices_inr.items())
print(tea_prices_npr)