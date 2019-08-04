import json
import re
import subprocess
import sys
import shlex


class KeybaseTeam:
    """Keybase Chat Client"""
    def __init__(self):
        self.base_cmd ='keybase team'

    def _send_team_api(self, api_command):
        """Send a JSON formatted request to the team api.

        This takes a dictionary and sends it as a JSON request to the Keybase
        team api. You can get a full list of supported API commands by running
        the following command in the terminal:
            keybase team api --help

        Args:
            api_command (dict): API command to send.

        Returns:
            dict: Response from API
        """
        command = "%s api -m '%s'" % (
            self.base_cmd,
            json.JSONEncoder().encode(api_command)
        )
        try:
            response = subprocess.check_output(shlex.split(command))
        except subprocess.CalledProcessError as err:
            raise

        return json.loads(response.decode('utf-8'))

    def _send_team_cmd(self, cmd):
        """added for future use if a api is not exposed"""
        command = '%s %s' % (self.base_cmd, cmd)
        with subprocess.Popen(
            shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ) as process:
            response = process.stdout.readlines()
        return response

    def add_members(self, team, usernames: list=None, emails: list=None) -> dict:
        """
        {
          "method": "add-members",
          "params": {
              "options": {
                  "team": "phoenix", 
                  "emails": [
                      {
                          "email": "alice@keybase.io", 
                          "role": "writer"
                      },
                      ...
                  ],
                  "usernames": [
                      {
                          "username": "frank",
                          "role": "reader"
                      },
                      {
                          "username": "keybaseio@twitter",
                          "role": "writer"
                      }
                  ]
                }
            }
        }
        """
        cmd = {
            "method": "add-members",
            "params": {
                "options": {
                    "team": team
                }
            }
        }
        if emails:
            cmd['params']['options']['email'] = emails
        if usernames:
            cmd['params']['options']['usernames'] = usernames

        return self._send_team_api(cmd)

    def remove_member(self, team, username: str) -> dict:
        """
        {
            "method": "remove-member",
            "params": {
                "options": {
                "team": "phoenix",
                "username": "frank"
                }
            }
        }
        """
        cmd = {
            "method": "remove-member",
            "params": {
                "options": {
                    "team": team,
                    "username": username
                }
            }
        }

        return self._send_team_api(cmd)

    def list_memberships(self, team):
        """
        {
            "method": "list-team-memberships",
            "params": {
                "options": {
                    "team": "phoenix"
                    }
                }
        }
        """
        cmd = {
            "method": "list-team-memberships",
            "params": {
                "options": {
                    "team": team
                }
            }
        }

        return self._send_team_api(cmd)
    
