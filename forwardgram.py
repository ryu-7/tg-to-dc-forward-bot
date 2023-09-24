from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel
import yaml
import sys
import logging
import subprocess
import os
import shutil


''' 
------------------------------------------------------------------------
                LOGGING - Initite logging for the Bot
------------------------------------------------------------------------
'''
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('telethon').setLevel(level=logging.WARNING)
logger = logging.getLogger(__name__)

''' 
------------------------------------------------------------------------
                Clear past media 
------------------------------------------------------------------------
'''
def del_dir(root_directory, prefix):
    for item in os.listdir(root_directory):
        item_path = os.path.join(root_directory, item)
        if os.path.isdir(item_path) and item.startswith(prefix):
            shutil.rmtree(item_path)

''' 
------------------------------------------------------------------------
    BOT FUNCTION - Everything that happens, happens for a reason
------------------------------------------------------------------------
'''
def start(config):
    # Telegram Client Init
    client = TelegramClient(config["session_name"],
                            config["api_id"],
                            config["api_hash"])
    # Telegram Client Start
    client.start()

    # Input Messages Telegram Channels will be stored in these empty Entities
    input_channels_entities = []
    output_channel_entities = []

    # Iterating over dialogs and finding new entities and pushing them to our empty entities list above
    for d in client.iter_dialogs():
        if d.name in config["input_channel_names"] or d.entity.id in config["input_channel_ids"]:
            input_channels_entities.append(InputChannel(d.entity.id, d.entity.access_hash))
        if d.name in config["output_channel_names"] or d.entity.id in config["output_channel_ids"]:
            output_channel_entities.append(InputChannel(d.entity.id, d.entity.access_hash))

    # Exit, don't wait for fire.
    if not output_channel_entities:
        logger.error(f"Could not find any output channels in the user's dialogs")
        sys.exit(1)

    if not input_channels_entities:
        logger.error(f"Could not find any input channels in the user's dialogs")
        sys.exit(1)

    # Use logging and print messages on your console.     
    logging.info(f"Forward Bot started. Listening on {len(input_channels_entities)} channels.")

    # Forwarding messages to {len(output_channel_entities)} channels.")

    # TELEGRAM NEW MESSAGE - When new message triggers, come here

    @client.on(events.NewMessage(chats=input_channels_entities))
    async def handler(event):

        # Get the sender's ID
        sender_id = event.message.sender_id
        # Access the message ID
        message_id = event.message.id

        # Get where the chat is from
        chat_from = event.chat if event.chat else (await event.get_chat())  # telegram MAY not send the chat enity
        chat_title = chat_from.title

        # Uncomment the line below to print full message in structured format on your console.
        # logging.info(f"Message: \n{event.message}")

        # We will parse the items from response. You can first view the full message above,
        # then decide which elements you want to parse from telegram response
        # If our entities contain URL, we want to parse and send Message + URL
        try:
            parsed_response = (event.message.message + '\n' + event.message.entities[0].url)
            parsed_response = ''.join(parsed_response)
        # Or else we only send Message
        except:
            parsed_response = event.message.message

        media_dir = "media_" + str(sender_id) + '_' + str(message_id)
        if event.message.media:
            os.makedirs(media_dir, exist_ok=True)
            await client.download_media(event.message, file=media_dir)

        # This is probably not the best way to do this but definitely the easiest way.
        # When message triggers you start discord messanger script in new thread and sends parsed input as sys.argv[1]
        subprocess.call([sys.executable, "discord_messager.py", str(parsed_response), str(chat_title), str(sender_id), str(message_id)])

        # This part is to forward message (text only, fix later) to telegram channels
        # for output_channel in output_channel_entities:
        #     # this will forward your message to channel_recieve in Telegram
        #     await client.forward_messages(output_channel, event.message)

        # Clear the media directory if exists
        del_dir("./", media_dir)

    client.run_until_disconnected()


''' 
------------------------------------------------------------------------
          MAIN FUNCTION - Can't dream without a brain ...
------------------------------------------------------------------------
'''

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        config = yaml.safe_load(f)
    del_dir("./", "media_")
    start(config)
