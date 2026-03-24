# Write a function that calculates sum of
# squares from 1 to 5 million.

# Run it:
#   sequentially for 4 inputs
#   using Pool with 4 processes for same inputs

# Compare and print both times.
# Prove multiprocessing is faster for CPU work.


# Sequentially Running :

import time
import multiprocessing


def sum_to_million(n):
    sum = 0
    for i in range(n):
        sum += (i + 1) ** 2
    # print(sum)
    return sum


# start = time.time()
# [sum_to_million(5000000) for i in range(5)]
# end = time.time()

# print(f"Time taken to run sequentially 4 times is {end - start} seconds")
# Time taken to run sequentially 4 times is 2.672586441040039 seconds


#! using pool with 4 processes for same inputs

if __name__ == "__main__":
    start = time.time()
    with multiprocessing.Pool(4) as p:
        results = p.map(sum_to_million, [5000000] * 4)
        print(results)
    end = time.time()
    print(f"Time taken to run 4 times with the help of  pool is {end - start} seconds")
[41666679166667500000, 41666679166667500000, 41666679166667500000, 41666679166667500000]
# Time taken to run 4 times with the help of  pool is 0.6466872692108154 seconds
