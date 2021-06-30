import asyncio

async def nested():
    return 42

async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    # b = nested()
    # print(b)
    # Let's do it differently now and await it:
    a = await nested()  # will print "42".
    print(a)
    return 1

print(asyncio.run(main()))
