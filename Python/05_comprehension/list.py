# List comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 12, 14, 17, 12234]


even_number = [number for number in numbers if number % 2 == 0]

# return "even" string instead of the number itself
result = ["even" for number in numbers if number % 2 == 0]

print(even_number)
print(result)

# comprehension
evens = [number for number in numbers if number % 2 == 0]

# exact same thing expanded
evens = []
for number in numbers:
    if number % 2 == 0:
        evens.append(number)  # ← this append is the first `number`
