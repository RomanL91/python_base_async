# ============================================================================
# синхронный вариант 
import requests

from time import time


def get_file(url):
    response = requests.get(
        url=url,
        allow_redirects=True,
        # cert=None
    )
    return response


def write_file(response):
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t_0 = time()
    url = 'https://loremflickr.com/320/240'
    
    for i in range(10):
        write_file(get_file(url))


    print(f'--->>> {time() - t_0}')


# if __name__ == '__main__':
#     main()


# ============================================================================
# асинхронный вариант 
import asyncio, aiohttp


def write_image(data):
    file_name = f'file-{int(time() * 1000)}.jpeg' 
    with open(file_name, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main_2():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)
        
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t_0 = time()
    asyncio.run(main_2())
    print(f'--время выполненеия->>> {time() - t_0}')
