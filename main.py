#!/usr/local/env/python3
import asyncio

from pykeybasebot import Bot, ContentType
from Private import Private

bot_name = "rudi9719"

active_teams = []

# An example module for PM'ing
bt = Private("private")
active_teams.append(bt)

class Handler:
    async def __call__(self, bot, event):
        if event.msg.content.type != ContentType.TEXT:
            return
        else:
            self.process_kbmsg(event.msg.channel.name, event.msg.sender.username,
                               event.msg.content.text.body, event.msg.channel.topic_name)

    def process_kbmsg(self, team, sender, message, channel):
        if isinstance(channel, str):
            if "@{}".format(bot_name) in message:
                if bot_name == sender:
                    pass
                else:
                    global team_found
                    team_found = False
                    print("{} said {} in @{}#{}".format(sender, message, team, channel))
                    for active_team in active_teams:
                        if team == active_team.team_name:
                            team_found = True
                            active_team.handle(channel, message, sender)
                    if not team_found:
                        bt.random_message(sender, team, channel)
        else:
            # Is a PM
            bt.random_message(sender=sender)



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
