import yaml
import sys
import logging
import discord

catagory_1 = [INPUT_CHANNEL_1_NAME, INPUT_CHANNEL_2_NAME]   # change catagory list
catagory_2 = [INPUT_CHANNEL_3_NAME]
catagory_3 = [INPUT_CHANNEL_4_NAME]

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
source_msg = "====================\nThis news is brought you by: " + source + '\n\n'
message = source_msg + message + "\n===================="

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

    print('We have logged in as {0.user}'.format(discord_client))
    print('Awaiting Telegram Message')

    # My channels are for RTX card drops and PS5
    channel_1 = discord_client.get_channel(config["discord_1_channel"])
    channel_2 = discord_client.get_channel(config["discord_2_channel"])
    channel_3 = discord_client.get_channel(config["discord_3_channel"])
    # channel_4 = discord_client.get_channel(config["discord_4_channel"])

    if source in catagory_1:
        await channel_1.send(message)
    elif source in catagory_2:
        await channel_2.send(message)
    elif source in catagory_3:
        await channel_3.send(message)

    sys.exit(0)
    # quit()

discord_client.run(config["discord_bot_token"])

    

    

