import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
from googletrans import Translator
from discord import Webhook
import aiohttp
import json
import re
import requests
import io

load_dotenv()
token = os.getenv("TOKEN")
dlx_url = os.getenv("DEEPLX_API")
use_dlx = int(os.getenv("USE_DEEPLX"))

logger = logging.getLogger("discord")

OPTED_OUT_USERS_FILE = "optedout.json"
intents = discord.Intents(guilds=True, messages=True, message_content=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

t = Translator()
bad_pings = ("@everyone", "@here")
tg_regex = r"^\*\*.*\*\*\n"
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
    
    gtranslated = t.translate(
        text=re.sub(
            pattern=tg_regex,
            repl='',
            string=message_text
        ),
        dest='en'
    )

    if gtranslated.src == "en":
        logger.info(f"translation of {message.id} not needed")
        return

    translated = gtranslated.text
    if use_dlx:
        data = {
            "text": message_text,
            "source_lang": gtranslated.src
        }
        deeplx_translate = requests.post(dlx_url, json.dumps(data))
        if deeplx_translate.status_code == 200:
            translated = json.loads(deeplx_translate.text)["data"]
        else:
            logger.info(f"{message.id}: deeplx api returned status code {deeplx_translate.status_code}, falling back to gtranslate")
            logger.info(f"{message.id}: deeplx api text output: {deeplx_translate.text}")

    # chr(10) returns the \n character, f-strings in python dont allow backslashes in the brace substitution parts
    formatted = f"{message_text}\n-# `{gtranslated.src} -> en` {translated.replace(chr(10), chr(10)+'-# ')}"

    wh_url = await message.channel.webhooks()
    if wh_url == []:
        logger.info(f"{message.id}: no webhooks for channel {message.channel.id} - automatically creating one")
        await message.channel.create_webhook(name="gloykinator translation webhook")
        wh_url = await message.channel.webhooks()
    wh_url = wh_url[0].url

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(wh_url, session=session)
        # if you set it to MISSING it wont do anything since thats the default variable definition in the function itself
        attachments = discord.utils.MISSING

        if message.author.id != webhook.id:
            logger.info(f"message {message.id} translated")
            if message.reference is not None:
                mentioned = f" {message.reference.resolved.author.mention}" if message.reference.resolved.author in message.mentions else ""
                formatted = f"> {message.reference.resolved.jump_url}{mentioned}\n" + formatted
            
            if message.attachments != []:
                attachments = []
                for attachment in message.attachments:
                    attachment_fp = io.BytesIO()
                    await attachment.save(attachment_fp)
                    attachments.append(discord.File(attachment_fp, attachment.filename))
            
            await message.delete()
            await webhook.send(
                content=formatted,
                username=message.author.name,
                avatar_url=message.author.avatar.url,
                files=attachments
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
