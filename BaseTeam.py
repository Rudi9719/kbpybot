import subprocess
import random


class BaseTeam:
    team_name = None

    def __init__(self, team_name):
        self.team_name = team_name

    def send_message(self, channel, message, team=None):
        if team:
            subprocess.run(["keybase", "chat", "send", team, message, "--channel", channel])
        else:
            subprocess.run(["keybase", "chat", "send", self.team_name, message, "--channel", channel])

    def handle(self, channel, message, sender):
        raise NotImplementedError

    def random_message(self, sender, team=None, channel=None):
        messages = [
            'Del Monte Green Beans.', 'I am not prepared for that.',
            'Help?', 'I got nothing..', 'Who are you?', 'Hush your buckets..',
            'A what? A stack?'
        ]
        message = random.choice(messages)
        if channel:
            subprocess.run(["keybase", "chat", "send", team, message, "--channel", channel])

        else:
            subprocess.run(["keybase", "chat", "send", sender, message])
