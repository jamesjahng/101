import asyncio
import os
from pprint import pprint
from pydaybit import Daybit, PARAM_API_KEY, PARAM_API_SECRET

async def daybit_markets():
    async with Daybit(params={PARAM_API_KEY: "",
                              PARAM_API_SECRET: ""}) as daybit:
        quote = 'USDT'
        base = 'BTC'
        pprint(await (daybit.trades / quote / base)(size=1))
while True:
    asyncio.get_event_loop().run_until_complete(daybit_markets())