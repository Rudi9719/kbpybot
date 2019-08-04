import io
import json
import re
import subprocess
import sys
import shlex


class KeybaseBot:
    def __init__(self, keybase_api, channels, help_command=r'^!help$',
                 help_trigger='!help', log_to_screen=True):
        """
        Args:
            keybase_api (Obj: KeybaseChat): Keybase chat API object
            channels (dict): List of teams and channels to use
            help_command (str): regex for help command
            help_trigger (str): trigger
            log_to_screen (bool): log output to screen
        """
        self._help_trigger = help_trigger
        self.command = self._command_registry()
        self.kb = keybase_api
        self.channels = channels
        self._commands[help_command] = {
                'f': self.help_cmd,
                'command': help_command,
                'help_trigger': help_trigger,
                'show_help': True,
                'help': self.help_cmd.__doc__
                }
        self.commands = self.get_commands()
        self.log_to_screen = log_to_screen

    def _command_registry(self, *args):
        self._commands = {}
        self._commands_list = [self._help_trigger]

        def make_command(*args, **kwargs):
            try:
                cmd = args[0]
            except IndexError:
                raise ValueError('Must provide command trigger')
            help_trigger = kwargs.get('help_trigger', cmd)
            show_help = kwargs.get('show_help', True)

            def decorator(func, *args, **kwargs):
                def wrapper(func):
                    self._command_name = cmd
                    self._commands_list.append(self._command_name)
                    self._commands[self._command_name] = {}
                    self._commands[self._command_name]['f'] = func
                    self._commands[self._command_name]['command'] = cmd
                    self._commands[self._command_name]['help_trigger'] = help_trigger
                    self._commands[self._command_name]['show_help'] = show_help
                    self._commands[self._command_name]['help'] = func.__doc__
                    return func
                return wrapper(func)
            return decorator
        return make_command

    def get_commands(self):
        return self._commands.copy()

    def _write_log(self, *log_message, error=False, **kwargs):
        clean_messages = ()
        for message in log_message:
            clean_message = str(message).encode('unicode-escape')
            clean_messages += (str(clean_message), )
        if self.log_to_screen:
            if not error:
                print(*clean_messages, **kwargs)
            else:
                print(*clean_messages, file=sys.stderr, **kwargs)

    def run(self, respond=True):
        """Run bot"""
        for message in self.kb.api_listener():
            if respond and '{' in message:
                message = json.loads(message)
                #print('channels: %s message: %s' % (self.channels.keys(), message))
                
                if message['msg']['content']['type'] != 'text':
                    continue
                found_cmd = [
                    cmd for cmd in self.get_commands()
                    if re.search(cmd, message['msg']['content']['text']['body'])
                ]
                if len(found_cmd) > 0:
                    trigger = found_cmd[0]
                    trigger_func = self.get_commands()[trigger]['f']
                    
                    if message['msg']['channel']['members_type'] == 'team':
                        # Skip unintended messages
                        if message['msg']['channel']['name'] not in self.channels.keys() or \
                                'topic_name' not in message['msg']['channel'].keys():
                            continue
                        # Not correct topic team support only
                        if message['msg']['channel']['topic_name'] not in \
                                self.channels[message['msg']['channel']['name']]:
                            continue

                        message_data = {
                            'type': message['msg']['channel']['members_type'],
                            'body': message['msg']['content']['text']['body'],
                            'sender': message['msg']['sender']['username'],
                            'team': message['msg']['channel']['name'],
                            'channel': message['msg']['channel']['topic_name']
                        }
                        result = trigger_func(message_data)
                        log_message = (
                            '-' * 15,
                            'Trigger found: {}'.format(trigger),
                            '  - Team: {}'.format(message_data['team']),
                            '  - Channel: {}'.format(message_data['channel']),
                            '  - Sender: {}'.format(message_data['sender']),
                            '  - Message: {}'.format(message_data['body']),
                            '  - Result -',
                            '    {}'.format(result)
                        )
                    elif message['msg']['channel']['members_type'] == 'impteamnative':
                        message_data = {
                            'type': message['msg']['channel']['members_type'],
                            'body': message['msg']['content']['text']['body'],
                            'sender': message['msg']['sender']['username']
                        }
                        result = trigger_func(message_data)
                        log_message = (
                            '-' * 15,
                            'Trigger found: {}'.format(trigger),
                            '  - Sender: {}'.format(message_data['sender']),
                            '  - Message: {}'.format(message_data['body']),
                            '  - Result -',
                            '    {}'.format(result))
                    self._write_log(*log_message, sep='\n', end='\n\n')

    def check_messages(self, respond=True):
        conversations = self.kb.get_conversations()

        # Respond to team messages
        teams = [team for team in conversations['teams']
                 if team in self.channels]
        for team in teams:
            unread_channels = [
                    channel for channel in self.channels[team]
                    if conversations['teams'][team][channel]['unread']
                    ]
            for channel in unread_channels:
                messages = self.kb.get_team_messages(team, channel=channel)
                for key, message in messages.items():
                    # message information
                    message_data = {
                            'type': 'team',
                            'body': message['body'],
                            'sender': message['sender'],
                            'team': team,
                            'channel': channel
                            }
                    if respond:
                        found_cmds = [cmd for cmd in self.get_commands()
                                      if re.search(cmd, message['body'])]
                        if len(found_cmds) > 0:
                            trigger = found_cmds[0]
                            trigger_func = self.get_commands()[trigger]['f']
                            result = trigger_func(message_data)
                            log_message = (
                                '-' * 15,
                                'Trigger found: {}'.format(trigger),
                                '  - Team: {}'.format(team),
                                '  - Channel: {}'.format(channel),
                                '  - Sender: {}'.format(message['sender']),
                                '  - Message: {}'.format(message['body']),
                                '  - Result -',
                                '    {}'.format(result))
                            self._write_log(*log_message, sep='\n', end='\n\n')

        # Respond to private messages
        users = [
                user for user in conversations['individuals']
                if conversations['individuals'][user]['unread']
                ]
        for user in users:
            messages = self.kb.get_user_messages(user)
            for key, message in messages.items():
                # message information
                message_data = {
                        'type': 'impteamnative',
                        'body': message['body'],
                        'sender': message['sender']
                        }
                if respond:
                    found_cmds = [cmd for cmd in self.get_commands()
                                  if re.search(cmd, message['body'])]
                    if len(found_cmds) > 0:
                        trigger = found_cmds[0]
                        trigger_func = self.get_commands()[trigger]['f']
                        result = trigger_func(message_data)
                        log_message = (
                            '-' * 15,
                            'Trigger found: {}'.format(trigger),
                            '  - Sender: {}'.format(message['sender']),
                            '  - Message: {}'.format(message['body']),
                            '  - Result -',
                            '    {}'.format(result))
                        self._write_log(*log_message, sep='\n', end='\n\n')

    def respond(self, response_text, message_data, at_mention=False, 
                                                nonblock=False):
        if message_data['type'] == 'team':
            _at = ''
            if at_mention:
                _at = '@{}, '.format(message_data['sender'])
            res = self.kb.send_team_message(message_data['team'],
                                            '{}{}'.format(
                                                _at,
                                                response_text),
                                            nonblock=nonblock,
                                            channel=message_data['channel'])
        elif message_data['type'] == 'impteamnative':
            res = self.kb.send_user_message(message_data['sender'],
                                            response_text,
                                            nonblock=nonblock)
        return json.dumps(res)

    def help_cmd(self, message_data):
        '''Show available commands'''
        help_text = ''
        all_cmds = self.get_commands()
        cmds_list = self._commands_list.copy()
        self._write_log('all_cmds', all_cmds)
        self._write_log('cmds_list', cmds_list)
        for cmd in all_cmds:
            if all_cmds[cmd]['show_help']:
                help_trigger = all_cmds[cmd]['help_trigger']
                cmd_help = all_cmds[cmd]['help']
                help_text += '`{}`\n'.format(help_trigger)
                help_text += '```    {}```\n\n'.format(cmd_help)
        if message_data['type'] == 'team':
            res = self.kb.send_team_message(message_data['team'],
                                            help_text,
                                            channel=message_data['channel'])
        elif message_data['type'] == 'impteamnative':
            res = self.kb.send_user_message(message_data['sender'],
                                            help_text)
        return json.dumps(res)

