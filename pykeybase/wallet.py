import json
import re
import subprocess
import sys
import shlex


class KeybaseWallet:
    """Keybase Chat Client"""
    def __init__(self):
        self.base_cmd ='keybase wallet'

    def _send_wallet_api(self, api_command):
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

    def _send_wallet_cmd(self, cmd):
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

    def balances(self):
        """List the balances in all your accounts:
            {"method": "balances"}
        """
        cmd = {
            "method": "balances"
        }

        return self._send_wallet_api(cmd)

    def history(self, account_id):
        """See payment history in an account:
            {
                "method": "history",
                "params": {
                    "options": {
                        "account-id": "GDUK..."
                    }
                }
            }"""
        cmd = {
            "method": "history",
            "params": {
                "options": {
                    "account-id": account_id
                }
            }
        }

        return self._send_wallet_api(cmd)

    def transaction_details(self, txid):
        """Get details about a single transaction:
            {
                "method": "details",
                "params": {
                    "options": {
                        "txid": "616dec04976c4..."
                    }
                }
            }"""
        cmd = {
            "method": "details",
            "params": {
                "options": {
                    "txid": txid
                }
            }
        }

        return self._send_wallet_api(cmd)

    def lookup_primary_account(self, user):
        """Lookup the primary Stellar account ID for a user:
            {
                "method": "lookup",
                "params": {
                    "options": {
                        "name": "patrick"
                    }
                }
            }"""
        cmd = {
            "method": "lookup",
            "params": {
                "options": {
                    "name": user
                }
            }
        }

        return self._send_wallet_api(cmd)

    def get_inflation(self, account_id):
        """Get the inflation destination for an account:
            {
                "method": "get-inflation",
                "params": {
                    "options": {
                        "account-id": "ESI2QL5UZHCK4"
                    }
                }
            }"""
        cmd = {
            "method": "get-inflation",
            "params": {
                "options": {
                    "account-id": account_id
                }
            }
        }

        return self._send_wallet_api(cmd)

    def send(self, user, amount, currency="XLM", message=""):
        """Send XLM to a keybase user (there is no confirmation so be careful):
            {
                "method": "send",
                "params": {
                    "options": {
                        "recipient": "patrick",
                        "amount": "1",
                        "currency": "USD",
                        "message": "here's the money I owe you"
                    }
                }
            }"""
        cmd = {
            "method": "send",
            "params": {
                "options": {
                    "recipient": user,
                    "amount": amount,
                    "currency": currency,
                    "message": message
                }
            }
        }

        return self._send_wallet_api(cmd)

    def setup(self):
        """Initialize the wallet for an account:
            {
                "method": "setup-wallet"
            }"""
        cmd = {
            "method": "setup-wallet"
        }

        return self._send_wallet_api(cmd)
