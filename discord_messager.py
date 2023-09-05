import yaml
import sys
import logging
import discord

''' 
------------------------------------------------------------------------
    DISCORD CLIENT - Init the client
------------------------------------------------------------------------
'''

discord_client = discord.Client(intents=discord.Intents.default())
with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)

''' 
------------------------------------------------------------------------
    MESSAGE AS WE RECIEVE FROM FORWARDGRAM SCRIPT
------------------------------------------------------------------------
'''

message = sys.argv[1]
source = sys.argv[2]
message = "This news is brought you by: " + source + '\n\n' + message + "\n===================="

'''
------------------------------------------------------------------------
    GET CHANNEL LIST
------------------------------------------------------------------------
'''
channel_ids = config["discord_channel_id"]
channel_cnt = len(channel_ids)
channel_src = []
for i in range(0, channel_cnt):
    tag = "channel_" + str(i+1) + "_source"
    channel_src.append(config[tag])

''' 
------------------------------------------------------------------------
    DISCORD SERVER START EVENT - We will kill this immaturely
------------------------------------------------------------------------
'''
# when discord is initalized, it will trigger this event. 
# we quickly send messages to our discord channels and quit the script prematurely.
# this gets trigged again when a new message is sent on channel from telegram

@discord_client.event
async def on_ready():

    for i in range(0, channel_cnt):
        if source in channel_src[i]:
            channel_client = discord_client.get_channel(channel_ids[i])
            await channel_client.send(message)

    # Set the traceback limit to 0 to suppress traceback output
    sys.tracebacklimit = 0

    # Exit the script without displaying any traceback or exception
    sys.exit()
    # quit()

discord_client.run(config["discord_bot_token"])