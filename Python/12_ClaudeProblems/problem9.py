# Find what's wrong with this code and fix it:

# async def fetch(url):
#     response = requests.get(url)
#     return response.text

# async def main():
#     results = await asyncio.gather(
#         fetch("https://httpbin.org/delay/1"),
#         fetch("https://httpbin.org/delay/1"),
#         fetch("https://httpbin.org/delay/1"),
#     )
#     print(results)

# asyncio.run(main())


# Fixed version :
# import asyncio
# import time

## import requests
# import aiohttp


# async def fetch(url, session):
#     # response = requests.get(url)
#     async with session.get(url) as response:
#         return response.text


# async def main():
#     async with aiohttp.ClientSession() as session:
#         start = time.time()
#         results = await asyncio.gather(
#             fetch("https://httpbin.org/delay/1", session),
#             fetch("https://httpbin.org/delay/1", session),
#             fetch("https://httpbin.org/delay/1", session),
#         )
#         end = time.time()
#         # print(results)
#         print(f"Total time :  {end - start}seconds")


# asyncio.run(main())
