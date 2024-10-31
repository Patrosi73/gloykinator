import os
import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger("discord")

intents = discord.Intents(guilds=True, messages=True, message_content=True, voice_states=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
token = os.getenv("TOKEN")

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        logger.info(f"message {message.id} is from the bot itself")
        return
    
    logger.info(f"translating message {message.id}")
    translate = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&dj=1&source=input&q={message.content}")
    gtranslate_result = json.loads(translate.text)

    if gtranslate_result["src"] == "en":
        print(gtranslate_result["src"])
        logger.info(f"translation of {message.id} not needed")
        return
    else:
        sentences = gtranslate_result['sentences']
        sentences_json = sentences[0]
        final_sentence = sentences_json['trans']

        logger.info(f"message {message.id} translated, sending")
        await message.channel.send(message.content + "\n-# `" + gtranslate_result["src"] + " -> en` " + final_sentence)

bot.run(token)
