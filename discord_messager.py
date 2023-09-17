import yaml
import sys
import discord
import os

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
sender_id = sys.argv[3]
message_id = sys.argv[4]

output_dict = {'msg': message,
               'src': source}

'''
------------------------------------------------------------------------
    GET CHANNEL LIST
------------------------------------------------------------------------
'''
channel_ids = config["discord_channel_id"]
channel_cnt = len(channel_ids)
channel_src = []
for i in range(0, channel_cnt):
    tag_source = "channel_" + str(i+1) + "_source"
    channel_src.append(config[tag_source])

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
            tag_format = "channel_" + str(i+1) + "_format"
            message = config[tag_format].format(**output_dict)

            media_dir = "./media_" + str(sender_id) + '_' + str(message_id) + '/'
            if os.path.exists(media_dir):

                media_list = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]

                # Create a list of discord.File objects
                media_files = [discord.File(os.path.join(media_dir, file_name)) for file_name in media_list]

            channel_client = discord_client.get_channel(channel_ids[i])
            # print("Sending to: {}".format(config['discord_channel_names'][i]))
            # print("message = '" + message + "'")

            await channel_client.send(message, files=media_files if os.path.exists(media_dir) else None)

    # Set the traceback limit to 0 to suppress traceback output
    sys.tracebacklimit = 0

    # Exit the script without displaying any traceback or exception
    sys.exit()
    # quit()

handler = None # logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord_client.run(config["discord_bot_token"], log_handler=handler)