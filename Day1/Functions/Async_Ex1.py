import time
import asyncio

async def async_function():
    print("This is a async function.")
    await asyncio.sleep(1)
    print("Finished executing async function.")

if __name__ == "__main__":
    asyncio.run(async_function())