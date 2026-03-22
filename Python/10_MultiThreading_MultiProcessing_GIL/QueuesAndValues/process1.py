import threading
import time


# Trying to crunch (count ) numbers using multiple threads
def cpu_heavy():
    print("Crunching some numbers")
    total = 0
    for _ in range(10**8):
        total += _
    print("Done ✅")


start = time.time()
threads = [threading.Thread(target=cpu_heavy) for _ in range(2)]
[t.start() for t in threads]
[t.join() for t in threads]
end = time.time()

print(f"Time taken :{end - start} seconds")
