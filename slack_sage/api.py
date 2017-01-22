import aiohttp

api = None


class APIContext:
    def __new__(cls, **kwargs):
        global api
        instance = super(APIContext, cls).__new__(cls)
        instance.api = api
        return instance

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __get___(self, obj, type=None):
        print(self)
        return self


class APIMethod:
    api = None

    def __get__(self, obj, type=None):
        self.api = obj
        return self


class RTM(APIMethod):
    async def start(self):
        return await self.api('rtm.start')


class Users(APIMethod):
    async def info(self, user_id):
        return await self.api('users.info', {'user': user_id})


class Channels(APIMethod):
    async def info(self, channel_id):
        return await self.api("channels.info", {'channel': channel_id})


class Groups(APIMethod):
    async def info(self, group_id):
        return await self.api("groups.info", {'channel': group_id})

class Chat(APIMethod):
    async def post_message(self, channel, text):
        return await self.api("chat.postMessage", {'text': text, 'channel': channel})


class SlackAPI:
    _token = None

    channels = Channels()
    chat = Chat()
    groups = Groups()
    users = Users()
    rtm = RTM()

    def __init__(self, token):
        global api
        api = self
        self._token = token
        assert self._token, "Token hasn't passed!"

    async def __call__(self, method, data=None):
        """Slack API call."""

        with aiohttp.ClientSession() as session:
            form = aiohttp.FormData(data or {})
            form.add_field('token', self._token)
            async with session.post('https://slack.com/api/{0}'.format(method),
                                    data=form) as response:
                assert 200 == response.status, ('{0} with {1} failed.'
                                                .format(method, data))
                return await response.json()
