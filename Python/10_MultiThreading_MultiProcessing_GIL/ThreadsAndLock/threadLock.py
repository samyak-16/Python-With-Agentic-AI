import threading

counter = 0
lock = threading.Lock()


def increament():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1


threads = [threading.Thread(target=increament) for _ in range(10)]
[t.start() for t in threads]
[t.join() for t in threads]

print(f"Final counter: {counter}")

# counter += 1 = three steps
#   step 1 → READ
#   step 2 → ADD
#   step 3 → WRITE

# GIL can switch after ANY of these steps
# it doesn't care that your operation isn't finished
# it just switches when its timer fires


# Thread 1: READ  counter = 0   ✅
# Thread 1: ADD   0 + 1 = 1     ✅
#           ← GIL SWITCHES (doesn't care Thread 1 isn't done!)

# Thread 2: READ  counter = 0   ← reads old value, Thread 1 hasn't written yet!
# Thread 2: ADD   0 + 1 = 1
# Thread 2: WRITE counter = 1
#           ← GIL SWITCHES BACK

# Thread 1: WRITE counter = 1   ← writes 1 again! Thread 2's work lost!

# counter = 1 ❌ should be 2


# "GIL doesn't wait for thread to complete all three steps"
# → correct, GIL fires on a timer, not on operation completion

# "in any middle of the three process it can switch context"
# → exactly, can switch after READ, after ADD, anywhere

# "another thread can interrupt with wrong count on memory"
# → yes, reads stale value that previous thread hadn't written yet

# "counting can be corrupted"
# → 100% — this is literally the definition of race condition


# Without lock:
#   GIL switches freely between steps
#   threads read stale values
#   writes overwrite each other
#   corruption ❌

# With lock:
#   Thread 1 acquires lock
#   GIL CANNOT give lock to Thread 2
#   Thread 2 waits outside
#   Thread 1 completes ALL three steps uninterrupted
#   Thread 1 releases lock
#   Thread 2 now goes — reads correct updated value ✅


#   Yes — GIL switches mid-operation without waiting for completion. Thread 1 can READ, then GIL switches, Thread 2 reads same stale value, both write same result, one operation lost. Lock prevents this by making all three steps one uninterruptible unit.
