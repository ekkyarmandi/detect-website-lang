import asyncio, aiohttp

# ignore event loop policy warnings
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# define the asyncfuntion
async def render(session, function, url):
    loop = asyncio.get_event_loop()
    try:
        async with session.get(url) as r:
            result = await loop.run_in_executor(None, function, url, await r.text())
            return result
    except:
        return None

async def gather(session, function, urls):
    tasks = []
    for url in urls:
        url = "https://" + url if "http" not in url else url
        task = asyncio.create_task(render(session, function, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def parse_all(function, urls):
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    async with aiohttp.ClientSession(headers=headers) as session:
        data = await gather(session, function, urls)
        return data