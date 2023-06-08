from __future__ import annotations

import asyncio
from random import random
import aiohttp
import os


tasks = []


async def download_cat(session: aiohttp.ClientSession, img_url: str, i: int):
    response = await session.get(img_url)
    img = await response.read()
    format = img_url[-3:]

    with open(f'cat{i + 1}.{format}', 'wb') as file:
        file.write(img)

    print(f'cat{i + 1}.jpg')


async def request():
    link = "https://api.thecatapi.com/v1/images/search?limit=10"

    session = aiohttp.ClientSession()
    response = await session.get(link)
    answer: list[dict[str, str | int]] = await response.json()

    for i in range(10):
        img_url = answer[i]['url']
        tasks.append(download_cat(session, img_url, i))
    await asyncio.gather(*tasks)

    await session.close()


def main():
    asyncio.run(request())


main()
