import subprocess
import random


class BaseTeam:
    team_name = None

    def __init__(self, team_name):
        self.team_name = team_name

    def send_message(self, message, sender=None, team=None, channel=None):
        if team is not None and channel is not None:
            subprocess.run(["keybase", "chat", "send", team, message, "--channel", channel])
        elif team is not None and channel is None:
            subprocess.run(["keybase", "chat", "send", team, message])
        else:
            subprocess.run(["keybase", "chat", "send", sender, message])

    def handle(self, message, sender, team=None, channel=None):
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
