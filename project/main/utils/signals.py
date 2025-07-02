import aiohttp

async def run_background_task_with_delay(obj_id: int):
    _url = f'http://65.108.242.208/run_background_task_with_delay?obj_id={obj_id}'
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession() as session:
        async with session.get(_url,
                            timeout=timeout) as response:
            pass