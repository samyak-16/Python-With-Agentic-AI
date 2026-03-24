# Python Concurrency Practice Problems

> Solve these one by one to perfect your understanding of Threading, Multiprocessing, and Async/Await.

---

## Multi Threading

### Problem 1 — Basic I/O Simulation
```
Create 5 threads, each simulating a DB query
with different delays (1s, 2s, 3s, 1s, 2s).
Print which query finished first.
Total time should be ~3s not 9s.
```

### Problem 2 — Race Condition Challenge
```
Create a shared counter starting at 0.
Spawn 10 threads each incrementing
counter 1000 times.

First run WITHOUT lock — observe wrong answer.
Then run WITH lock — observe correct answer (10000).
Print both results and explain why they differ.
```

### Problem 3 — Producer Consumer
```
One thread produces numbers 1-10
(with 0.5s delay between each).
Another thread consumes them
and prints "consumed: X".
Use Queue for communication between them.
```

---

## Multi Processing

### Problem 4 — CPU Speedup Proof
```
Write a function that calculates sum of
squares from 1 to 5 million.

Run it:
  sequentially for 4 inputs
  using Pool with 4 processes for same inputs

Compare and print both times.
Prove multiprocessing is faster for CPU work.
```

### Problem 5 — Process Communication
```
Spawn 3 processes.
Each process calculates square of a number
(1, 2, 3) and sends result back to main process.
Main process collects all results using Queue
and prints them.
```

### Problem 6 — Shared Value
```
Spawn 4 processes each incrementing
a shared Value 500 times.

First WITHOUT lock — observe wrong answer.
Then WITH get_lock() — observe correct answer (2000).
Same as Problem 2 but for processes.
```

---

## Async / Await

### Problem 7 — Basic Gather
```
Write 3 async functions simulating API calls:
  fetch_users()    — takes 1s
  fetch_orders()   — takes 2s
  fetch_products() — takes 1.5s

Run them sequentially first — note time (~4.5s)
Then run with gather() — note time (~2s)
Print results of all three.
```

### Problem 8 — Async File Downloader
```
Use aiohttp to download these 3 URLs simultaneously:
  "https://httpbin.org/delay/1"
  "https://httpbin.org/delay/2"
  "https://httpbin.org/delay/1"

Print status code and time taken for each.
Total time should be ~2s not 4s.
Use one shared session.
```

### Problem 9 — Spot The Bug
```
Find what's wrong with this code and fix it:

async def fetch(url):
    response = requests.get(url)
    return response.text

async def main():
    results = await asyncio.gather(
        fetch("https://httpbin.org/delay/1"),
        fetch("https://httpbin.org/delay/1"),
        fetch("https://httpbin.org/delay/1"),
    )
    print(results)

asyncio.run(main())
```

---

## Boss Level — Combine Everything

### Problem 10 — Real World Pipeline
```
Build a simple data pipeline:

Step 1 (async)        → fetch 3 URLs simultaneously using aiohttp
                         collect their status codes

Step 2 (threading)    → simulate saving each result to DB
                         3 threads, each sleeps 1s (simulating DB write)
                         use Lock to safely append to shared results list

Step 3 (multiprocess) → take the results list
                         spawn 3 processes
                         each process counts characters in its result
                         return counts via Queue

Print final counts from all 3 processes.
```

---

## Recommended Order

| Order | Problem | Concept |
|-------|---------|---------|
| 1st | Problem 1 | Basic threading warmup |
| 2nd | Problem 2 | Race condition — core concept |
| 3rd | Problem 4 | Multiprocessing speedup proof |
| 4th | Problem 7 | Basic async gather |
| 5th | Problem 3 | Producer consumer pattern |
| 6th | Problem 5 | Process communication |
| 7th | Problem 8 | Real async HTTP |
| 8th | Problem 6 | Shared value + lock |
| 9th | Problem 9 | Spot the bug |
| 10th | Problem 10 | Everything combined |

---

> Solve them one by one. Share your code for review after each one. 🚀