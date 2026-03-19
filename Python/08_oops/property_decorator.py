# # @property lets you access a method like an attribute — no () needed when calling it:
# class TeaLeaf:
#     def __init__(self, age):
#         self._age = age

#     @property
#     def age(self):
#         return self._age + 2

#     @age.setter
#     def age(self, age):
#         if 1 <= age <= 5:
#             self._age = age

#         else:
#             raise ValueError("Tea leaf must be between 1-5 years .. ")


class BankAccount:
    def __init__(self, balance):
        self.balance = balance  # hits the setter

    @property
    def balance(self):  # GETTER — runs when you READ  acc.balance
        return self._balance

    @balance.setter
    def balance(self, value):  # SETTER — runs when you WRITE acc.balance = x
        if value < 0:
            raise ValueError("Balance can't be negative!")
        self._balance = value  # actual storage


acc = BankAccount(1000)
print(acc.balance)  # ✅ clean — no ()
acc.balance = 500  # ✅ clean — hits setter, validates
acc.balance = -100  # ❌ ValueError — protected!


# _balance to protect from infinite loops in getter and setter :)