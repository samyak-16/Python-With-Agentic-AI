# Spawn 4 processes each incrementing
# a shared Value 500 times.

# First WITHOUT lock — observe wrong answer.
# Then WITH get_lock() — observe correct answer (2000).
# Same as Problem 2 but for processes.


#! Without Lock :
# from multiprocessing import Process


# count = 0  # lives in main process memory


# def increase_value():
#     global count
#     count += 500


# if __name__ == "__main__":
#     processes = [Process(target=increase_value) for _ in range(4)]
#     [process.start() for process in processes]
#     [process.join() for process in processes]

#     print(
#         f"Final count is {count}"
#     )  # prints the value of count from  main process memory which is always 0


# With Lock :
from multiprocessing import Process, Value


def increase_value(count):
    with count.get_lock():
        count.value += 500


if __name__ == "__main__":
    count = Value("i", 0)
    processes = [Process(target=increase_value, args=(count,)) for _ in range(4)]
    [process.start() for process in processes]
    [process.join() for process in processes]

    print(
        f"Final count is {count.value}"
    )  # prints the value of count from  main process memory which is always 0
