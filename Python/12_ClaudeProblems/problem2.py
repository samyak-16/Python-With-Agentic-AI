# Create a shared counter starting at 0.
# Spawn 10 threads each incrementing
# counter 1000 times.

# First run WITHOUT lock — observe wrong answer.
# Then run WITH lock — observe correct answer (10000).
# Print both results and explain why they differ.
import threading

lock = threading.Lock()
count = 0


def counting_1000():
    global count
    for _ in range(1000):
        with lock:
            count += 1


init = [threading.Thread(target=counting_1000) for i in range(10)]

# print(init)
[t.start() for t in init]
[t.join() for t in init]

print("Final count is ", count)
