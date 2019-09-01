from BaseTeam import BaseTeam


class Private(BaseTeam):

    def __init__(self, team_name):
        super().__init__(team_name)

    def handle(self, message, sender, team=None, channel=None):
        if sender is not None:
            self.random_message(sender)
        else:
            super().handle(message=message, sender=sender, team=self.team_name, channel=channel)
