#!/usr/local/env/python3
import subprocess
import json
import threading
import os
import time

from BaseTeam import BaseTeam

bot_name = ""
active_teams = []

bt = BaseTeam("private")
active_teams.append(bt)


def main():
    global kbproc
    kbproc = subprocess.Popen(["keybase", "chat", "api-listen", "--hide-exploding"], universal_newlines=True, bufsize=1,
                              stdout=subprocess.PIPE)

    while True:

        kbmsg = str(kbproc.stdout.readline())
        if not kbmsg:
            if kbproc.poll() is not None:
                kbproc = subprocess.Popen(["keybase", "chat", "api-listen", "--hide-exploding"],
                                          universal_newlines=True, bufsize=1,
                                          stdout=subprocess.PIPE)
        else:
            threading.Thread(target=process_kbmsg(kbmsg)).start()
            kbproc.stdout.flush()


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


main()
