from multiprocessing import Process

# Process class lets us create child processes
import time


def count_numbers():
    # this function will run inside a child process
    # completely isolated — own memory, own GIL, own interpreter
    print("Started the count process..")
    count = 0
    for _ in range(100000000):  # counts to 100 million (heavy CPU work)
        count += 1
        # print(count)
    print("Ended the count process..")


# everything below runs in the PARENT process (main script)

if __name__ == "__main__":
    # guard is required because when child processes are spawned
    # they re-import this script
    # without this guard they would also hit Process().start()
    # and spawn more children forever → infinite loop → crash 💥

    start = time.time()

    # create two child processes
    # at this point they are just CREATED, not started yet
    # target = which function the child should run
    core1 = Process(target=count_numbers)
    core2 = Process(target=count_numbers)

    # NOW the child processes actually spawn
    # OS creates two brand new Python interpreters
    # each gets own memory copy, own GIL, own core (if available)
    # both start running count_numbers() independently
    core1.start()
    core2.start()

    # parent process WAITS here until core1 finishes
    # without join() parent would finish and exit
    # while children are still running
    core1.join()
    core2.join()

    end = time.time()

    # by here both children have finished their work
    print(f"All Process completed in {end - start} seconds")


## Full Summary
"""
Parent Process
  → the main script itself
  → the one YOU run with python script.py
  → creates and manages child processes

Child Process
  → brand new Python interpreter spawned by parent
  → completely isolated (own memory, own GIL, own core)
  → runs ONE specific function (count_numbers here)
  → doesn't share anything with parent or siblings
  → dies when its function finishes

Process(target=fn)  →  create a child (not started yet)
.start()            →  actually spawn it, OS assigns it a core
.join()             →  parent waits for child to finish

Why multiprocessing here?
  → count_numbers is pure CPU work (no I/O, no waiting)
  → threading won't help (GIL blocks parallel CPU work)
  → multiprocessing gives each process its own GIL
  → both truly run in parallel on separate cores
  → cuts time roughly in half

Why if __name__ == "__main__"?
  → child processes re-import your script to find the function
  → without guard they would also hit .start() and spawn more children
  → infinite spawning → system crash
  → guard says "skip this block if you are a child, not the main script"
"""
