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
        self.tts_channel_id = 1354208945128079551
        intents = discord.Intents.all()
        super().__init__(intents=intents) # make sure we inherit the init of discord.Client as well as its methods

    def starts_vowel(self, word):
        if word[0] in ["a", "e", "i", "o", "u"]:
            return True
        else:
            return False

    async def on_ready(self):
        
        object_detection_channel_id = self.get_channel(1345218942028873840)
        await object_detection_channel_id.send(f"# Waiting for image. Type 'HELP' for help.", tts=True)
        await self.get_channel(self.tts_channel_id).send(content="Waiting for image. Type 'HELP' for help.")

        text_recognition_channel_id = self.get_channel(1351256813814677654)
        await text_recognition_channel_id.send(f"# Waiting for image. Type 'HELP' for help.", tts=True)

    async def on_message(self, message):

        if message.author == self.user: 
            return

        if message.content.lower() == "help":
            await message.reply(content="# To take an image, press the 'plus' icon on the bottom left of the screen, the press the camera icon.", tts=True)

        if message.channel.id == 1345218942028873840:

            if message.attachments != []:
                url = message.attachments[0].url
                objects, annotated_image_np_arr = detector.get_objects(url, showimage=False)

                img_encode = cv2.imencode(".jpg", annotated_image_np_arr)[1] # convert the np array to a jpg
                image_bytes = io.BytesIO(img_encode) 
                image_bytes.seek(0) # start from beginning of stream

                if len(objects) == 1:
                    if self.starts_vowel(objects[0].lower()) == False:
                        await message.reply(content="# There is a " + objects[0] + " in front of you.", tts=True) # await basically allows other functions to run at the same time, this speaks out objects in photo
                        await self.get_channel(self.tts_channel_id).send(content="There is a " + objects[0] + " in front of you.")
                    else:   
                        await message.reply(content="# There is an " + objects[0] + " in front of you.", tts=True)
                        await self.get_channel(self.tts_channel_id).send(content="There is an " + objects[0] + " in front of you.")

                elif len(objects) != 0:
                    if "person" in objects:
                        objects.remove("person")
                        if len(objects) == 1:
                            if self.starts_vowel(objects[0].lower()) == False:
                                await message.reply(content="# There is a " + objects[0] + " in front of you.", tts=True)
                                await self.get_channel(self.tts_channel_id).send(content="There is a " + objects[0] + " in front of you.")
                            else:
                                await message.reply(content="# There is an " + objects[0] + " in front of you.", tts=True)
                                await self.get_channel(self.tts_channel_id).send(content="There is an " + objects[0] + " in front of you.")
                        else:
                            await message.reply(content="# These are the objects in front of you: " + ", ".join(objects), tts=True)
                            await self.get_channel(self.tts_channel_id).send(content="These are the objects in front of you: " + ", ".join(objects))

                else:
                    await message.reply(content="# No objects detected.", tts=True)

                await message.add_reaction('👍')
                if objects != []:
                    img_file = await message.reply(file=discord.File(image_bytes, filename=str(message.author))) 

                    img_file_url = img_file.attachments[0].url

                    embed = discord.Embed(
                        color=discord.Colour.fuchsia() 
                    )

                    embed.set_image(url=img_file_url)
                    await message.channel.send(embed=embed)

                await message.channel.send("# Waiting for image.", tts=True)
                await self.get_channel(self.tts_channel_id).send(content="waiting for image")

        if message.channel.id == 1351256813814677654:

            if message.attachments != []:
                url = message.attachments[0].url
                
                if detector.get_text(url) != "No recognised text.":
                    await message.reply(f"# {detector.get_text(url)}", tts=True)
                    await self.get_channel(self.tts_channel_id).send(f"{detector.get_text(url)}")
                                                                                           
bot = ListenerBot()
bot.run(BOT_TOKEN)
