import asyncio
import json

import aiohttp

from slack_sage import handlers
from slack_sage import api


class SlackSage:
    api = None
    token = None

    def __init__(self, token):
        self.token = token
        self.api = api.SlackAPI(token)
        print(self.api)

    async def run(self):
        rtm = await self.api.rtm.start()
        assert rtm['ok'], "Error connecting to RTM."

        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(rtm["url"]) as ws:
                async for msg in ws:
                    assert msg.tp == aiohttp.WSMsgType.TEXT
                    message = json.loads(msg.data)
                    asyncio.ensure_future(self.handle(message))

    async def handle(self, message):
        await handlers.process_handlers(message)
        # if message.get('type') == 'message' and message.get('subtype') != 'bot_message':
        #     m = Message.parse(message)
        #     channel_info = await m.channel.info
        #     user_info = await m.user.info
        #     # print(channel)
        #
        #     info = await m.channel.post_message("Hello!")
        #     print("{0}: {1}".format(user_info["user"]["name"],
        #                             message["text"]))
        # else:
        #     print(message, file=sys.stderr)
