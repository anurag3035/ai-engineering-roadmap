import asyncio
import aiohttp
import time

urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/posts/4",
    "https://jsonplaceholder.typicode.com/posts/5"
]

async def fetch_data(session, url):
    try:
        async with asyncio.timeout(5):
            async with session.get(url) as response:
                data = await response.json()
                print(f"Fetched data from {url}")
                return data

    except asyncio.TimeoutError:
        print(f"Request timed out for {url}")

    except Exception as e:
        print(f"Error: {e}")

async def concurrent_fetch():
    async with aiohttp.ClientSession() as session:
        tasks = []

        for url in urls:
            tasks.append(fetch_data(session, url))

        results = await asyncio.gather(*tasks)
        return results

async def sequential_fetch():
    async with aiohttp.ClientSession() as session:
        results = []

        for url in urls:
            result = await fetch_data(session, url)
            results.append(result)

        return results

async def main():

    print("Starting sequential execution...")

    start_time = time.perf_counter()
    await sequential_fetch()
    sequential_time = time.perf_counter() - start_time

    print(f"Sequential execution time: {sequential_time:.2f} seconds")

    print("\nStarting concurrent execution...")

    start_time = time.perf_counter()
    await concurrent_fetch()
    concurrent_time = time.perf_counter() - start_time

    print(f"Concurrent execution time: {concurrent_time:.2f} seconds")

    if concurrent_time > 0:
        print(
            f"Concurrent version is "
            f"{sequential_time / concurrent_time:.2f}x faster"
        )

if __name__ == "__main__":
    asyncio.run(main())