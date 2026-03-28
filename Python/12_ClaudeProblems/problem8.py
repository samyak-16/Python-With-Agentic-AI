# Use aiohttp to download these 3 URLs simultaneously:
#   "https://httpbin.org/delay/1"
#   "https://httpbin.org/delay/2"
#   "https://httpbin.org/delay/1"

# Print status code and time taken for each.
# Total time should be ~2s not 4s.
# Use one shared session.


import aiohttp
import asyncio
import time


async def download_url(session, url):
    start = time.time()
    async with session.get(url) as response:
        print(response.status)
        # data = await response.json()
    end = time.time()

    print(f"Time taken is {end - start} seconds")


async def main():
    async with aiohttp.ClientSession() as session:
        listt = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/delay/1",
        ]
        tasks = [download_url(session, url) for url in listt]
        total_start = time.time()
        await asyncio.gather(*tasks)  # ✅ Fire all at once, wait for ALL
        total_end = time.time()

        print(f"\nTotal time: {total_end - total_start:.2f}s")  # ~2s not 4s


asyncio.run(main())
