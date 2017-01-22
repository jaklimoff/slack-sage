from slack_sage import api


class SlackUser(api.APIContext):
    user_id = None
    username = None

    @property
    async def info(self):
        return await self.api.users.info(self.user_id)


