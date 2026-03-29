# Build a simple data pipeline:

# Step 1 (async)        → fetch 3 URLs simultaneously using aiohttp
#                          collect their status codes

# Step 2 (threading)    → simulate saving each result to DB
#                          3 threads, each sleeps 1s (simulating DB write)
#                          use Lock to safely append to shared results list

# Step 3 (multiprocess) → take the results list
#                          spawn 3 processes
#                          each process counts characters in its result
#                          return counts via Queue

# Print final counts from all 3 processes.


import aiohttp
import asyncio
import threading
import time
from multiprocessing import Process, Queue

lock = threading.Lock()
results = []


async def fetch(url, session):
    async with session.get(url) as response:
        print(f"Response : {response.status}")
        return await response.text()


def saveDb(data):

    time.sleep(1)
    with lock:
        results.append(data)


async def task():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3",
    ]
    async with aiohttp.ClientSession() as session:
        coroutinee = [fetch(url, session) for url in urls]
        texts = await asyncio.gather(*coroutinee)
        # print(texts)

        threadss = [threading.Thread(target=saveDb, args=(data,)) for data in texts]
        [t.start() for t in threadss]
        [t.join() for t in threadss]


# print(results)


def returnCharacterCount(q, data):

    q.put(len(data))


def main():
    asyncio.run(task())
    q = Queue()
    processes = [
        Process(target=returnCharacterCount, args=(q, data)) for data in results
    ]
    [p.start() for p in processes]
    [p.join() for p in processes]
    for i in range(3):
        print(f"Character count for process {i+1} : {q.get()}")


if __name__ == "__main__":
    main()
