import asyncio
import subprocess
import json
import re
import sys
import shlex


class AsyncKeybaseChat:
    """Keybase Chat Client"""
    def __init__(self):
        self.base_cmd = 'keybase chat'
        self.username = self._get_username()

    async def _send_chat_api(self, api_command):
        """Send a JSON formatted request to the chat api.

        This takes a dictionary and sends it as a JSON request to the Keybase
        chat api. You can get a full list of supported API commands by running
        the following command in the terminal:
            keybase chat api --help

        Args:
            api_command (dict): API command to send.

        Returns:
            dict: Response from API
        """
        command = r"%s api -m '%s'" % (
            self.base_cmd,
            json.JSONEncoder().encode(api_command).replace("'", "'\"'\"'")
        )
        cmd_list = shlex.split(command) 
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdout=asyncio.subprocess.PIPE
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()

        return json.loads(stdout.decode('utf-8'))
    
    def _get_username(self):
        """Return the username of the current user from the keybase CLI.
           TODO:
            * Check for errors if user is not logged in
        """
        command = subprocess.check_output(['keybase', 'status', '-j'])
        keybase_status = json.loads(command.decode('utf-8'))
        return keybase_status.get('Username')

    @staticmethod
    async def api_listener():
        """api_listener() generator function around the api listener"""
        command = 'keybase chat api-listen'
        cmd_list = command.split()
        process = await asyncio.create_subprocess_exec(
            *cmd_list,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        while True:
            line = await process.stdout.readline()
            yield line.decode().strip()
    
    async def send_team_message(self, team, message, nonblock=True,
                            channel='general'):
        """Send message to a team channel.

        Args:
            team (str): Team name
            message (str): Message to send to the channel

        Optional Args:
            channel (str): Channel name within the team

        Returns:
            dict: Response from API
        """
        api_command = {
            "method": "send",
            "params": {
                "options": {
                    "channel": {
                        "name": team,
                        "members_type": "team",
                        "topic_name": channel
                    },
                    "message": {
                        "body": message
                    },
                    "nonblock": nonblock
                }
            }
        }
        return await self._send_chat_api(api_command)

    async def send_user_message(self, user, message, nonblock=True):
        """Send message to a single user.

        Args:
            user (str): User's username
            message (str): Message to send to the user

        Returns:
            dict: Response from API
        """
        api_command = {
            "method": "send",
            "params": {
                "options": {
                    "channel": {
                        "name": "{},{}".format(self.username, user)
                    },
                    "message": {
                        "body": message
                    },
                    "nonblock": nonblock
                }
            }
        }
        resp = await self._send_chat_api(api_command)
        return resp


