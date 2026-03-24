# Create 5 threads, each simulating a DB query
# with different delays (1s, 2s, 3s, 1s, 2s).
# Print which query finished first.
# Total time should be ~3s not 9s.


import threading
import time


def query_to_db(t):
    time.sleep(t)


# Time simulation :

simulation = (1, 2, 3, 1, 2)  # seconds

queries_thread = [
    threading.Thread(target=query_to_db, args=(time,), name=f"{time}")
    for time in simulation
]
start = time.time()
print("Starting the thread")
[t.start() for t in queries_thread]
[t.join() for t in queries_thread]
end = time.time()

print(f"Task Completed after : {end - start} seconds")
