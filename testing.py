import volcanic.test
import asyncio
if __name__ == '__main__':
    asyncio.run(volcanic.test.amc.launchTransportsAsync())
    print(volcanic.test.amc)
    # asyncio.get_event_loop().run_forever()