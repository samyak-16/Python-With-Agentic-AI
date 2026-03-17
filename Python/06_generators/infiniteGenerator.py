def infinite_counter(start=0):
    n = start
    while True:        # ← runs forever
        yield n
        n += 1

counter = infinite_counter()

print(next(counter))  # 0
print(next(counter))  # 1
print(next(counter))  # 2
# ... forever