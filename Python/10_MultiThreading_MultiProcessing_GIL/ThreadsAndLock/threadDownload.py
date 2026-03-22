import threading
import requests
import time


def download(url):
    print(f"Starting download from {url}")
    resp = requests.get(url)  # I/O operation — HTTP request
    # GIL released while waiting for response
    # other threads run during this wait
    print(f"Finished {url} — size: {len(resp.content)} bytes")


urls = [
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/svg",
]

start = time.time()

threads = []
for url in urls:
    t = threading.Thread(target=download, args=(url,))  # ✅ tuple
    t.start()
    threads.append(t)  # ✅ append not push

for t in threads:
    t.join()

end = time.time()
print(f"All downloads in {end - start} seconds")


##! Why Threading Works Perfectly Here

# This is a textbook I/O bound task —
# ```
# Thread 1 → sends request to httpbin.org/image/png
#            waiting for response...
#            GIL released ← key moment

# Thread 2 → grabs GIL → sends request to httpbin.org/image/jpeg
#            waiting for response...
#            GIL released

# Thread 3 → grabs GIL → sends request to httpbin.org/image/svg
#            waiting for response...
#            GIL released

# All three waiting simultaneously
# whoever gets response first → grabs GIL → processes it
# ```
# ```
# Without threading:
#   download url1 → wait → done
#   download url2 → wait → done
#   download url3 → wait → done
#   Total: ~3 seconds

# With threading:
#   download url1 ┐
#   download url2 ┤ all waiting simultaneously
#   download url3 ┘
#   Total: ~1 second (slowest single download)
# ```

# ---

# ## The GIL Connection Here
# ```
# requests.get(url)
# → sends HTTP request
# → now just WAITING for server response
# → GIL automatically released during this wait
# → other threads jump in and send their requests
# → all three requests are in flight simultaneously
# → GIL only needed again when response arrives
#    and Python processes the data
# ```

# This is exactly why threading helps for I/O — CPU is idle during network wait, GIL gets released, other threads use that idle time.

# ---

# ## One Line Summary
# ```
# Why threading works here:
#   network request = I/O = GIL released while waiting
#   all three requests fly out simultaneously
#   total time = slowest single download, not sum of all
