# Process  =  program currently running
#             (Chrome running, VS Code running, your Python script running)

# Thread   =  list of tasks inside that program
#             actual work that gets sent to CPU

import threading
import time


def boil_milk():
    print(f"Boiling the milk ..{'.'}")
    time.sleep(2)
    print("Milk boiled")


def toast_bun():
    print("Tosting the bun")
    time.sleep(3)
    print("Done with bun toast .. ")


start = time.time()
t1 = threading.Thread(target=boil_milk)
t2 = threading.Thread(target=toast_bun)
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()

print(f"BreakFast is ready in {end - start} seconds..")
