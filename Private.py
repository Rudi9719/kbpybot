from BaseTeam import BaseTeam

class Private(BaseTeam):

    def __init__(self, team_name):
        super().__init__(team_name)

    def handle(self, channel, message, sender):
        self.random_message(sender)