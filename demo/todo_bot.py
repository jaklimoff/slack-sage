import asyncio
import json
import os

import re

from slack_sage.bot import SlackSage
from slack_sage.handlers import DirectMessageHandler

# Create bot instance
bot = SlackSage(os.environ['SLACK_API_TOKEN'])

todos = {}


class CreateTodo(DirectMessageHandler):
    """
    Create todo if the are any input in direct message,
    but if the input is list or delete - ignore this input
    byt regex
    """
    trigger_messages = [r"\w+"]
    exclude_commands = [r"^list$", r"^delete \d+$"]  # Exclude this command

    async def process(self):
        if todos.get(self.message.user.user_id) is None:
            todos[self.message.user.user_id] = []

        user_todos = todos[self.message.user.user_id]
        new_task = self.message.text
        user_todos.append(new_task)

        await self.message.channel.post_message(
            "Hey! I add <{task}> as task. There are {tasks_count} in your list.".format(
                task=new_task,
                tasks_count=len(user_todos)
            ))


class ListTodos(DirectMessageHandler):
    trigger_messages = [r"^list$"]  # trigger only by `list` command

    async def process(self):
        user_todos = todos.get(self.message.user.user_id, [])

        attachments = []

        for idx, ut in enumerate(user_todos):
            task = dict()
            task['title'] = "#%s" % idx
            task['text'] = ut
            task['mrkdwn_in'] = ["text"]
            task['actions'] = [
                {
                    "name": "done",
                    "text": "Done",
                    "style": "primary",
                    "type": "button",
                    "value": "done"
                },
                {
                    "name": "delete",
                    "text": "Delete",
                    "type": "button",
                    "style": "danger",
                    "value": "delete"
                }
            ]
            attachments.append(task)

        a = await self.message.channel.post_message(attachments=json.dumps(attachments))
        print(a)


class DeleteTodos(DirectMessageHandler):
    trigger_messages = [r"^delete \d+"]  # trigger only by `list` command

    async def process(self):
        user_todos = todos.get(self.message.user.user_id, [])
        digits_found = re.findall(r'(\d+)', self.message.text)
        if digits_found:
            task_id = int(digits_found[0])
            try:
                task = user_todos[task_id]
                user_todos.__delitem__(task_id)
                await self.message.channel.post_message("Deleted! <%s> :(" % task)
            except IndexError:
                await self.message.channel.post_message("No such task! :(")




loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(bot.run())
loop.close()
