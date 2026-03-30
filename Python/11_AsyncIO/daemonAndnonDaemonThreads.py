import threading
import time


def non_daemon_task():
    time.sleep(3)
    print("Non-daemon done")  # WILL print


def daemon_task():
    time.sleep(5)
    print("Daemon done")  # might NOT print — gets killed early


t1 = threading.Thread(target=non_daemon_task)  # daemon=False by default
t2 = threading.Thread(target=daemon_task, daemon=True)

t1.start()
t2.start()

print("Main thread done")
# t2 gets killed here since main + all non-daemons are done
# t1 keeps program alive for 3 more seconds
