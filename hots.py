import asyncio
import enum

import aiohttp


class Region(enum.Enum):
    US = 1
    EU = 2
    KR = 3
    CN = 5


# TODO: Actual object
class Player:
    def __repr__(self):
        return str(self.__dict__)


class HOTSAPI:
    def __init__(self, loop: asyncio.AbstractEventLoop = None, sess: aiohttp.ClientSession = None):
        self.loop = loop or asyncio.get_event_loop()
        self.sess = sess or aiohttp.ClientSession(loop=self.loop)

    async def player(self, battletag: str, region: Region) -> Player:
        url = 'https://api.hotslogs.com/Public/Players/{}/{}'.format(region.value, battletag.replace('#', '_'))
        async with self.sess.get(url) as resp:
            data = await resp.json()
            if data:
                p = Player()
                p.__dict__.update((k.lower(), v) for k, v in data.items())
                return p

    async def global_player(self, battletag: str) -> Player:
        for region in Region:
            data = await self.player(battletag, region)
            if data:
                return data
