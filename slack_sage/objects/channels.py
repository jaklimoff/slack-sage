from slack_sage import api


class ChannelTypes:
    PRIVATE_CHANNEL = 1
    PUBLIC_CHANNEL = 2
    DIRECT_MESSAGE = 3


class Channel(api.APIContext):
    channel_id = None
    type = None

    @property
    async def info(self):
        # TODO: Optimize this
        if self.channel_id.startswith("C"):
            self.type = ChannelTypes.PUBLIC_CHANNEL
            return await self.api.channels.info(self.channel_id)
        elif self.channel_id.startswith("G"):
            self.type = ChannelTypes.PRIVATE_CHANNEL
            return await self.api.groups.info(self.channel_id)
        elif self.channel_id.startswith("D"):
            self.type = ChannelTypes.DIRECT_MESSAGE
            return await self.api.groups.info(self.channel_id)

    async def post_message(self, text="", **kwargs):
        return await self.api.chat.post_message(self.channel_id, text, **kwargs)