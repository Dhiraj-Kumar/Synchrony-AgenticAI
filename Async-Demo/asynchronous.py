import asyncio
import time
import aiohttp


async def fetch_user(user_id):
    print(f"Fetching data for user: {user_id}")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://jsonplaceholder.typicode.com/users/{user_id}"
        ) as response:
            return await response.json()

async def main():
    start = time.time()
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    end = time.time()

    print(f"Total time: {end-start:.2f} seconds")

asyncio.run(main())