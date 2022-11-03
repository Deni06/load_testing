import asyncio
import json

import aiohttp


async def get(
    session: aiohttp.ClientSession,
    color: int,
    **kwargs
) -> dict:
    body = {
        "type": "text",
        "text": {
            "body": "https://facebook.com"
        },
        "unique_id": "pkOgidNs7R",
        "waid": str(color),
        "profile_name": "Deni",
        "channel_id": 2116,
        "room_id": "60993003"
    }
    body = json.dumps(body)
    headers = {'content-type': 'application/json'}
    url = "http://localhost:8080/checking_hashtag"
    resp = await session.post(url, headers=headers, data=body)
    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    data = await resp.json()
    print(f"Received data for {url}")
    return data


async def main(**kwargs):
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with aiohttp.ClientSession() as session:
        tasks = []
        x = range(80)
        for n in x:
            tasks.append(get(session=session, color=n, **kwargs))
        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    asyncio.run(main())  # Python 3.7+