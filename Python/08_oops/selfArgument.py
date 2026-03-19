class Chaicup:
    size = 150 
    def describe(self):
        # print(self) # See what self is :)
        return f"A {self.size} ml chai cup"
    
cup = Chaicup()

print(cup.describe())
print(Chaicup.describe()) # Error required 1positional argument but passed none
print(Chaicup.describe(cup)) # first argument is always the reference to the instance 