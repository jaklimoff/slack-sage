import asyncio
import json
import os

from slack_sage.mixins import RequestsMixin
from slack_sage.bot import SlackSage
from slack_sage.handlers import AllChannelsHandler

# Create bot instance
bot = SlackSage(os.environ['SLACK_API_TOKEN'])


# Create some handlers
class RedditNews(AllChannelsHandler, RequestsMixin):
    trigger_messages = [r"reddit"]

    async def process(self):
        response = await self.get("https://www.reddit.com/r/webdev/.json")
        r_json = json.loads(response)
        last_article = r_json.get('data', {}).get('children', [])[0].get('data')
        await self.message.channel.post_message("{title} ({url})".format(**last_article))


loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(bot.run())
loop.close()
