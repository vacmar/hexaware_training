import asyncio

async def task_1():
    print("Starting Task 1")
    await asyncio.sleep(2)
    print("Finished Task 1")

async def task_2():
    print("Starting Task 2")
    await asyncio.sleep(1)
    print("Finished Task 2")

async def main():
    await asyncio.gather(task_1(), task_2())

if __name__ == "__main__": 
    asyncio.run(main())
    
