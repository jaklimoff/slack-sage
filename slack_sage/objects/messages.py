from slack_sage import api
from . import user
from . import channels


class Message(api.APIContext):
    user = None
    channel = None
    text = None

    @staticmethod
    def parse(obj):
        return Message(
            channel=channels.Channel(channel_id=obj.get('channel')),
            user=user.SlackUser(user_id=obj.get('user')),
            text=obj.get('text')
        )
