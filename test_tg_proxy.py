import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.telegram.org",
            proxy="socks5://127.0.0.1:10808"
        ) as resp:
            print(resp.status)
            print(await resp.text())

asyncio.run(main())
