import asyncio

import fakeredis

redis = fakeredis.FakeStrictRedis()
redis.set("temperature", 0)


# sample furniture, assume external
async def stove():
    while True:
        temperature = int(redis.get("temperature"))
        redis.set("temperature", temperature + 1)
        await asyncio.sleep(1)


# control function, assume external
async def cooling_stove():
    while True:
        temperature = int(redis.get("temperature"))
        if temperature > 10:
            redis.set("temperature", temperature - 1)
        await asyncio.sleep(1)


'''
async def stove_temperature():
    while True:
        temperature = int(redis.get("temperature"))
        print(temperature)
        await asyncio.sleep(1)
'''


async def main():
    await asyncio.gather(stove(), cooling_stove())
    # await asyncio.gather(stove(), cooling_stove(), stove_temperature())


if __name__ == '__main__':
    asyncio.run(main())
