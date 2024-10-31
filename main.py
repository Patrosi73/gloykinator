import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
from googletrans import Translator
from discord import Webhook
import aiohttp
import json

load_dotenv()
logger = logging.getLogger("discord")
OPTED_OUT_USERS_FILE = "optedout.json"

intents = discord.Intents(guilds=True, messages=True, message_content=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
token = os.getenv("TOKEN")

t = Translator()
bad_pings = ("@everyone", "@here")
try:
    opted_out = json.load(
        open(OPTED_OUT_USERS_FILE, "r+")
    )
except:
    logger.info("optedout.json is non-existant or empty...")
    opted_out = {"users": []}

async def setup_hook() -> None:
    await bot.tree.sync()
bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        logger.info(f"message {message.id} is from the bot itself")
        return
    elif message.author.id in opted_out["users"]:
        logger.info(f"message {message.id} is from an opted-out user")
        return
    
    logger.info(f"translating message {message.id}")
    message_text = message.content
    for i in bad_pings:
        message_text = message_text.replace(i, "")
    
    translated = t.translate(message_text, dest='en')

    if translated.src == "en":
        logger.info(f"translation of {message.id} not needed")
        return
    else:
        formatted = f"{message_text}\n-# `{translated.src} -> en` {translated.text}"

        wh_url = await message.channel.webhooks()
        if wh_url == []:
            logger.info(f"no webhooks for channel {message.channel.id}")
            await message.delete()
            if os.getenv("IGNORE_NOWEBHOOK") == "1":
                formatted = "***psst!! i don't have a webhook to send to! create one in channel settings to make this look way nicer***\n\n" + formatted
                await message.channel.send(formatted)
            return
        wh_url = wh_url[0].url

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(wh_url, session=session)
            if message.author.id != webhook.id:
                logger.info(f"message {message.id} translated")
                if message.reference is not None:
                    formatted = f"> {message.reference.resolved.jump_url}\n" + formatted
                await message.delete()
                await webhook.send(
                    content=formatted,
                    username=message.author.name,
                    avatar_url=message.author.avatar.url
                )
            else:
                logger.info(f"message {message.id} is from webhook")

@bot.tree.command(name="opt-out", description="Opts you out from automatic translation.")
async def opt_out(interaction: discord.Interaction) -> None:
    if interaction.user.id in opted_out["users"]:
        await interaction.response.send_message("You are already opted out.")
    else:
        opted_out["users"].append(interaction.user.id)
        json.dump(
            obj=opted_out,
            fp=open(OPTED_OUT_USERS_FILE, "w")
        )
        await interaction.response.send_message("Opted out successfully.")

@bot.tree.command(name="opt-in", description="Opts you back into automatic translation.")
async def opt_out(interaction: discord.Interaction) -> None:
    if interaction.user.id in opted_out["users"]:
        opted_out["users"].remove(interaction.user.id)
        json.dump(
            obj=opted_out,
            fp=open(OPTED_OUT_USERS_FILE, "w")
        )
        await interaction.response.send_message("Opted in successfully.")
    else:
        await interaction.response.send_message("You are currently opted in (default). Do `/opt-out` to opt out.")

bot.run(token)
