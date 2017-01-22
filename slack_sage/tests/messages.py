import unittest
from slack_sage import handlers
from slack_sage.handlers import MetaHandler
from slack_sage.tests.base import BaseAsyncTestCase, AsyncMock
from unittest.mock import MagicMock, patch


class TestHandlers(BaseAsyncTestCase):
    def setUp(self):
        self.MESSAGE = {'type': 'message',
                        'channel': 'G3UQB7HGD',
                        'user': 'U0JJHA4KV',
                        'text': 'reddit',
                        'ts': '1485086805.000090',
                        'team': 'T0JJG7AMB'}

    async def test_handlers_process(self):
        class TestHandler(handlers.PrivateChannelMessageHandler):
            def process(self):
                pass

        old_handlers = MetaHandler.handlers

        mock = AsyncMock()
        TestHandler.process = mock
        MetaHandler.handlers = [TestHandler]

        # Must be called because it is message in private channel
        self.MESSAGE['channel'] = 'G3UQB7HGD'
        await handlers.process_handlers(self.MESSAGE)
        self.assertEqual(mock.called, 1)

        # Message in public channel. TestHandler won't be called
        self.MESSAGE['channel'] = 'C3UQB7HGD'
        await handlers.process_handlers(self.MESSAGE)
        self.assertEqual(mock.called, 1)

        MetaHandler.handlers = old_handlers

    async def test_private_channel_handler(self):
        class TestHandler(handlers.PrivateChannelMessageHandler):
            def process(self):
                pass

        self.MESSAGE['channel'] = 'G3UQB7HGD'
        self.assertTrue(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'C3UQB7HGD'
        self.assertFalse(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'D3UQB7HGD'
        self.assertFalse(await TestHandler.validate(self.MESSAGE))

    async def test_public_channel_handler(self):
        class TestHandler(handlers.PublicChannelMessageHandler):
            def process(self):
                pass

        self.MESSAGE['channel'] = 'C3UQB7HGD'
        self.assertTrue(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'G3UQB7HGD'
        self.assertFalse(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'D3UQB7HGD'
        self.assertFalse(await TestHandler.validate(self.MESSAGE))

    async def test_direct_channel_handler(self):
        class TestHandler(handlers.DirectMessageHandler):
            def process(self):
                pass

        self.MESSAGE['channel'] = 'D3UQB7HGD'
        self.assertTrue(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'G3UQB7HGD'
        self.assertFalse(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'C3UQB7HGD'
        self.assertFalse(await TestHandler.validate(self.MESSAGE))

    async def test_all_channel_handler(self):
        class TestHandler(handlers.AllChannelsHandler):
            def process(self):
                pass

        self.MESSAGE['channel'] = 'D3UQB7HGD'
        self.assertTrue(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'G3UQB7HGD'
        self.assertTrue(await TestHandler.validate(self.MESSAGE))

        self.MESSAGE['channel'] = 'C3UQB7HGD'
        self.assertTrue(await TestHandler.validate(self.MESSAGE))
