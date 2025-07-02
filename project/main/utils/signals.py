import aiohttp

async def run_background_task_with_delay(send_name: str):
    _url = f'http://65.108.242.208/run_background_task_with_delay?name_send={send_name}'
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession() as session:
        async with session.get(_url,
                            timeout=timeout) as response:
            pass