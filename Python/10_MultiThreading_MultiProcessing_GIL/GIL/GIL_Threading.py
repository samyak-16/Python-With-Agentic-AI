# Cores — CPU broken into multiple physical sections, each can do real work. ✅

# Thread — a list of tasks/code that needs to be executed, one by one. ✅
# One core, one thread at a time — exactly right. ✅

# Context switching — turn by turn in milliseconds, saving state so work isn't lost, making it feel simultaneous. ✅

# GIL reason — memory conflict, multiple threads accessing same memory address at same time could corrupt data. ✅


# Core
#   → physical section of CPU
#   → does the actual execution
#   → 8 cores = 8 things truly running at same moment

# Thread
#   → a sequence / list of code to be executed
#   → software concept, lives in RAM
#   → can be thousands of them

# Context Switching
#   → OS switches threads on a core every ~1ms
#   → saves current thread state (bookmark)
#   → loads next thread state
#   → so fast it feels simultaneous
#   → this is CONCURRENCY (illusion of parallel)

# GIL (Global Interpreter Lock)
#   → one single lock for the ENTIRE Python interpreter
#   → not per core — applies across ALL cores
#   → only ONE thread can execute Python code at a time
#   → exists because Python uses reference counting for memory
#   → if two threads modified same memory simultaneously
#     → count corrupts → wrong memory freed → crash
#   → GIL is released during I/O (network, DB, file)
#     → that's why threading still helps for I/O work
#   → escape it with multiprocessing
#     → each process = own interpreter = own GIL
#     → now all 8 cores actually work

import time
import threading


def CountingNumbers():
    print(f"{threading.current_thread().name} started counting")
    count = 0
    for i in range(100000000):
        count += 1
    print(f"{threading.current_thread().name} ended counting")


thread_1 = threading.Thread(target=CountingNumbers, name="Thread 1")
thread_2 = threading.Thread(target=CountingNumbers, name="Thread 2")

start = time.time()
thread_1.start()
# thread_2.start()

thread_1.join()
# thread_2.join()
end = time.time()

print(f"total time taken : {end - start}seconds")
