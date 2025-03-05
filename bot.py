# next steps: format return arr in get_objects properly, consider using specific coordinate positions

# import required libaries
import discord
import os
from dotenv import load_dotenv
from main import ComputerVision
import numpy as np
import cv2
import io

# create image detection object instance
detector = ComputerVision()

load_dotenv() # loading bot token from .env file
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

class ListenerBot(discord.Client):
    
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents) # make sure we inherit the init of discord.Client as well as its methods

    async def on_ready(self):
        general_channel_id = self.get_channel(1345218942028873840)
        await general_channel_id.send(f"Waiting for image. Type 'HELP' for help.", tts=True)

    async def on_message(self, message):

        if message.author == self.user: # do not do anything with bot's own messages
            return

        if message.content.lower() == "help":
            await message.reply(content="To take an image, press the 'plus' icon on the bottom left of the screen, the press the camera icon.", tts=True)
        
        if message.attachments != []:
            url = message.attachments[0].url
            objects, annotated_image_np_arr = detector.get_objects(url, showimage=False)

            img_encode = cv2.imencode(".jpg", annotated_image_np_arr)[1] #convert the np array to a jpg
            image_bytes = io.BytesIO(img_encode) # bytesio object to store in memory 
            image_bytes.seek(0) # make sure we start from the start of the stream

            if len(objects) == 1:
                await message.reply(content="There is a " + objects[0] + "in front of you.", tts=True) # await basically allows other functions to run at the same time, this speaks out objects in photo

            else:
                await message.reply(content=objects, tts=True)

            # let's adjust these messages to make sure they work^^^ also need to format objects correctly.
            await message.add_reaction('👍')
            img_file = await message.reply(file=discord.File(image_bytes, filename=str(message.author))) #discord.File opens the fiel in 'rb' mode to read the bytes

            img_file_url = img_file.attachments[0].url #img_file is a message object

            embed = discord.Embed( #embed tuple
                color=discord.Colour.fuchsia() # change this into a high contrast neon colour so client can easily see wher embed is
            )

            embed.set_image(url=img_file_url)
            await message.channel.send(embed=embed)

            await message.channel.send("Waiting for image.", tts=True)
                                                                                           
bot = ListenerBot()
bot.run(BOT_TOKEN)
