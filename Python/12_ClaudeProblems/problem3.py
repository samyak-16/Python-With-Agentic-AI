# One thread produces numbers 1-10
# (with 0.5s delay between each).
# Another thread consumes them
# and prints "consumed: X".
# Use Queue for communication between them.

import threading
import time
from queue import Queue

q = Queue()


def producer():
    for i in range(1, 11):
        time.sleep(0.5)
        print(f"Produced {i}")
        q.put(i)


def consumer():
    for _ in range(10):
        item = q.get()
        print(f"Consumed {item}")
        q.task_done()


t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()
t1.join()
t2.join()
