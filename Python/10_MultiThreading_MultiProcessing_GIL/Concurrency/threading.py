# Threading example


# Physical CPU cores  →  the actual workers, can only do ONE thing at a time

# Threads             →  sequences of code waiting to be worked on
#                        could be 5 lines, could be 1000 lines, doesn't matter
#                        just independent chunks of work

# Context switching   →  core works on Thread 1 for a few ms
#                        pauses it, saves where it left off
#                        picks up Thread 2, works on it for a few ms
#                        pauses it, goes back to Thread 1...
#                        so fast it FEELS like everything runs together

# Multi-threading     →  your program has multiple of these
#                        independent sequences running "at the same time"


import threading
import time


def my_task(name):
    print(f"{name} is running")
    time.sleep(1)


# Creat a thread

t = threading.Thread(target=my_task, args=("Task-1",))

# Start it - OS now schedules it on a core
t.start()
#  Wait for it to finish before moving on
t.join()
# Waits here until the thred work is completed the goes to next block of code - It blocks all the program

print("Done")
