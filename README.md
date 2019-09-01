# kbpybot
Another Keybase Bot framework in Python

Well... Not really. (I'm using the official Keybase Bot library)

# Idea
Make a Keybase Bot with minimal API Interaction that is extendable via subclasses of the main BaseTeam
Allow the bot to be configured more precisely using modules. I also wanted a bot that isn't controlled via a command prefix.
To issue a command to this bot, you would prefix with the bot's @username.

# Problems thus far
My main loop was causing the Keybase process to devour CPUs.
This was fixed by leveraging the official Keybase Python Bot Library.
I didn't like how interaction with the library worked, so I wrote my wrapper to simplify it.

# Running
To run the bot, you must supply a bot_name to the main.py and run the bot on a machine/user with Keybase logged in.
In the future I may implement starting the bot with a paper key, and/or configuration via YAML.

# ToDo
* Implement ACLs using YAML or Keybase Commands and designate an owner in the main config

* Rewrite send_message() to use the API as documented from Keybase's @dxb Kaco tool

* Threads? (AsyncIO, GIL vs Threads. Trying to make it efficient?)

* Use the new Bot API to broadcast commands


# dxb
dxb wuz hear
