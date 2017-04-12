from slack_sage.logger import slack_logger
from slack_sage.objects.messages import Message
import re


class Handlers:
    i = 0

    def __init__(self, handlers, message):
        self.message = message
        self.handlers = handlers

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= len(self.handlers):
            raise StopAsyncIteration
        else:
            h = self.handlers[self.i]
            self.i += 1
            if await h.validate(self.message):
                handler = h(self.message)
                await handler.prepare()
                return handler
            else:
                return await self.__anext__()


class MetaHandler(type):
    handlers = []

    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""
        handler = cls
        if MetaHandler.__module__ != handler.__module__:
            # Called when a plugin class is imported
            MetaHandler.handlers.append(cls)
            # return handler


async def process_handlers(message):
    slack_logger.debug(message)
    async for h in Handlers(MetaHandler.handlers, message):
        await h.process()


class BaseHandler(metaclass=MetaHandler):
    """
    Base Handler for all event triggers
    """
    msg = None

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    @classmethod
    async def validate(cls, msg):
        """
        Return True if handler must aggregate this message
        :param msg: Message from slack WS
        :return: bool
        """
        return True

    async def prepare(self):
        pass

    async def process(self):
        raise NotImplementedError("You must implement this method to process handlers")


class MessageHandler(BaseHandler):
    trigger_messages = [r".*"]  # Set here ytour trigger messages
    exclude_commands = []  # Exclude this command

    message = None  # type: Message

    @classmethod
    async def validate(cls, msg):
        is_message = msg.get('type') == "message" and msg.get('subtype') != 'bot_message'
        matched_trigger = False
        matched_exclude_commands = False

        if is_message:
            msg_text = msg.get('text')

            for tm in cls.trigger_messages:
                matched_trigger = re.match(tm, msg_text) is not None
                if matched_trigger:
                    break

            for tm in cls.exclude_commands:
                matched_exclude_commands = re.match(tm, msg_text) is not None
                if matched_exclude_commands:
                    break

        return is_message and (matched_trigger and not matched_exclude_commands)

    async def prepare(self):
        self.message = Message.parse(self.msg)


class DirectMessageHandler(MessageHandler):
    channel = None
    user = None

    @classmethod
    async def validate(cls, msg):
        return await super(DirectMessageHandler, cls).validate(msg) and msg.get('channel').startswith("D")


class PublicChannelMessageHandler(MessageHandler):
    channel = None
    user = None

    @classmethod
    async def validate(cls, msg):
        return await super(PublicChannelMessageHandler, cls).validate(msg) and msg.get('channel').startswith("C")


class PrivateChannelMessageHandler(MessageHandler):
    channel = None
    user = None

    @classmethod
    async def validate(cls, msg):
        return await super(PrivateChannelMessageHandler, cls).validate(msg) and msg.get('channel').startswith("G")


class AllChannelsHandler(DirectMessageHandler, PublicChannelMessageHandler, PrivateChannelMessageHandler):
    @classmethod
    async def validate(cls, msg):
        return await super(PrivateChannelMessageHandler, cls).validate(msg)
