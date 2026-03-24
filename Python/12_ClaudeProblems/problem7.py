# Write 3 async functions simulating API calls:
#   fetch_users()    — takes 1s
#   fetch_orders()   — takes 2s
#   fetch_products() — takes 1.5s

# Run them sequentially first — note time (~4.5s)
# Then run with gather() — note time (~2s)
# Print results of all three.


import asyncio
import time


async def fetch_users():
    await asyncio.sleep(1)


async def fetch_orders():
    await asyncio.sleep(2)


async def fetch_products():
    await asyncio.sleep(1.5)


# #! Running them sequentially
# start = time.time()
# asyncio.run(
#     fetch_users()
# )  # main thread blocked for 1s :  Creates a brand new event loop each time so no use of it no any benifits
# asyncio.run(
#     fetch_orders()
# )  # main thread blocked for 2s: Creates a brand new event loop each time so no use of it no any benifits
# asyncio.run(
#     fetch_products()
# )  # main thread blocked for 1.5s: Creates a brand new event loop each time so no use of it no any benifits
# end = time.time()

# print(f"All function runned sequentially in {end - start} seconds")
# # All function runned sequentially in 4.537063121795654 seconds


#! Running them using gather()


async def main():

    return await asyncio.gather(fetch_users(), fetch_orders(), fetch_products())


start = time.time()

result = asyncio.run(main())
"""

asyncio.run(main())
```
```
asyncio.run()     →  creates the event loop
                      puts main() coroutine inside it
                      starts the loop

    main() runs
        │
        asyncio.gather()  →  just takes 3 coroutine objects
                              registers all 3 on the ALREADY EXISTING event loop
                              nothing new created

        event loop now manages all 3 concurrently

asyncio.run()     →  loop finishes, destroys it"""

end = time.time()

print(f"All function runned using gather in {end - start} seconds")
print(f"Result : {result}")

# All function runned using gather in 2.016298294067383 seconds
