# attribute Shadowing

class Chai :
    temperature = 'hot'
    strength = "Strong"

cutting = Chai()
cutting.cup = "Big"
cutting.temperature = "Mild" # Custom temperature is added 
print("Before deletion",cutting.temperature) # Mild
del cutting.temperature
del cutting.cup

print("After deletion",cutting.temperature) # Hot

# Error comes here cause there is no any fallback in the u[per class level]

print(cutting.cup)