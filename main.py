#!/usr/local/env/python3
import asyncio

from pykeybasebot import Bot, ContentType
from Private import Private

bot_name = ""
owner_name = ""
active_teams = []

# An example module for PM'ing
bt = Private("private")
active_teams.append(bt)

team_found = False  # For the loop below


# Process the kbmsg from Keybase's API
def process_kbmsg(message, sender, team, channel):
    if sender != bot_name:
        if isinstance(channel, str):
            if "@{}".format(bot_name) in message:
                global team_found
                team_found = False
                print("{} said {} in @{}#{}".format(sender, message, team, channel))
                for active_team in active_teams:
                    if team == active_team.team_name:
                        team_found = True
                        active_team.handle(message, sender, channel)
                if not team_found:
                    bt.send_message("I don't belong here.", team=team, channel=channel)

        else:
            # Is a PM
            print("{} said {}".format(sender, message))


class Handler:
    async def __call__(self, bot, event):
        if event.msg.content.type != ContentType.TEXT:
            return
        else:
            process_kbmsg(event.msg.content.text.body, event.msg.sender.username,
                          event.msg.channel.name, event.msg.channel.topic_name)


listen_options = {
    'local': True,
    'wallet': True,
    'dev': True,
    'hide-exploding': False,
    'filter_channel': None,
    'filter_channels': None,
}
bot = Bot(
    username=bot_name,
    handler=Handler(),
)
asyncio.run(bot.start(listen_options))
