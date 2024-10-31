import os
import discord
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv
import logging
from googletrans import Translator

load_dotenv()
logger = logging.getLogger("discord")

intents = discord.Intents(guilds=True, messages=True, message_content=True, voice_states=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
token = os.getenv("TOKEN")
t = Translator()

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        logger.info(f"message {message.id} is from the bot itself")
        return
    
    logger.info(f"translating message {message.id}")
    translated = t.translate(message.content, dest='en')

    if translated.src == "en":
        logger.info(f"translation of {message.id} not needed")
        return
    else:
        logger.info(f"message {message.id} translated, sending")
        await message.channel.send(message.content + "\n-# `" + translated.src + " -> en` " + translated.text)

bot.run(token)
