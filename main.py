import os
import discord
from discord.ext import commands
import requests
import json
intents = discord.Intents(guilds=True, messages=True, message_content=True, voice_states=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    print(message.author)
    if message.author == bot.user:
        print("message is from the bot itself")
        return
    translate = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&dj=1&source=input&q={message.content}")
    print("getting translation")
    print(translate.text)
    gtranslate_result = json.loads(translate.text)
    if gtranslate_result["src"] == "en":
        print(gtranslate_result["src"])
        print("translation not needed")
        return
    else:
        print(gtranslate_result["src"])
        print("attempting translation")
        # this originally was for deeplx but it Does Not Work
        #data = {
        #    "text": message,
        #    "source_lang": gtranslate_result["src"].upper(),
        #   "target_lang": "EN-US"
         #
        #}
        sentences = gtranslate_result['sentences']
        sentences_json = sentences[0]
        final_sentence = sentences_json['trans']
        print("attempting to send message")
        await message.channel.send(message.content + "\n-# `" + gtranslate_result["src"] + " -> en` " + final_sentence)









bot.run(token)
