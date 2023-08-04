import asyncio

# ============================================================================
# простой пример для Python 3.4
@asyncio.coroutine
def print_nums():
    num = 1
    while True:
        print(num )
        num += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f'Прошло сек {count}')
        count += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def main():
    task_1 = asyncio.ensure_future(print_nums())
    task_2 = asyncio.ensure_future(print_time())

    yield from asyncio.gather(task_1, task_2)


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()

# ============================================================================

# ============================================================================
# простой пример для Python 3.5
async def print_nums():
    num = 1
    while True:
        print(num )
        num += 1
        await asyncio.sleep(1)


async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f'Прошло сек {count}')
        count += 1
        await asyncio.sleep(1)


async def main():
    # task_1 = asyncio.ensure_future(print_nums())
    # task_2 = asyncio.ensure_future(print_time())

    task_1 = asyncio.create_task(print_nums()) # Python 3.6
    task_2 = asyncio.create_task(print_time()) # Python 3.6

    await asyncio.gather(task_1, task_2)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    asyncio.run(main()) # Python 3.7

# ============================================================================

