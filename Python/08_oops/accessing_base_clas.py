# 3 ways to access base class

class Chai:
    def __init__(self,type_,strength):
        self.type = type_
        self.strength = strength

# Code  Duplication method


# class GingerChai(Chai):
#     def __init__(self,type_,strength,spice_level):
#         self.type = type_
#         self.strength = strength
#         self.spice_level = spice_level


# class GingerChai(Chai):
#     def __init__(self,type_,strength,spice_level):
#           # at this point, 'self' is a GingerChai instance
#         # sitting in memory, currently empty

#         Chai.__init__(self,type_,strength)
#         self.spice_level = spice_level
#          # you're passing THAT SAME GingerChai instance
#         # into Chai's __init__

        #! self never changes. It's the same object in memory throughout. You're just passing its reference into Chai.__init__ so Chai can write attributes onto it.


class GingerChai(Chai):
    def __init__(self, type_, strength, spice_level):
        super().__init__(type_, strength)
        self.spice_level = spice_level