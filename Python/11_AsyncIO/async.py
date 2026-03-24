import asyncio


async def make_coffee():
    print("boiling water...")
    await asyncio.sleep(3)
    print("Coffee ready !!!!!!!!!")


async def make_toast():
    print("toasting bread...")
    await asyncio.sleep(2)
    print("toast ready !!!!!!!!!")


async def main():
    # await asyncio.gather(
    #     make_coffee(),
    #     make_toast(),

    # )
    await asyncio.gather(
        make_coffee(),
        make_toast(),
    )


print(make_toast())  # <coroutine object make_toast at 0x000002691268EEC0>

# coroutine == Promise in JS , it represents a task which will complete in the future :

asyncio.run(main())
