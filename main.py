#!/usr/local/env/python3
import subprocess
import json
import os
import asyncio
import threading

from pykeybasebot import Bot, ContentType
from BaseTeam import BaseTeam
from Private import Private

bot_name = ""

active_teams = []

# An example module for PM'ing
bt = Private("private")
active_teams.append(bt)

class Handler:
    async def __call__(self, bot, event):
        if event.msg.content.type != ContentType.TEXT:
            return
        else:
           print(event) 

    def process_kbmsg(kbmsg):
        kbobj = json.loads(kbmsg)
        if "text" not in kbobj["msg"]["content"]["type"]:
            return
        sender = kbobj["msg"]["sender"]["username"]
        message = kbobj["msg"]["content"]["text"]["body"]
        team = kbobj["msg"]["channel"]["name"]  # Not sure why, channel is msg.channel.topic_name
        if bot_name in kbobj["msg"]["channel"]["name"]:
            # If someone PM's the bot
            bt.random_message(sender=sender)
        elif "@{}".format(bot_name) in message:
            # Don't reply to myself.
            if "{}".format(bot_name) in sender:
                return
            # Not a PM or from bot
            channel = kbobj["msg"]["channel"]["topic_name"]
            global team_found
            team_found = False
            print("{} said {} in @{}#{}".format(sender, message, team, channel))
            for active_team in active_teams:
                if team == active_team.team_name:
                    team_found = True
                    threading.Thread(target=active_team.handle(channel, message, sender)).start()
            if not team_found:
                bt.random_message(sender, team, channel)
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
