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
async def on_ready(self):
    print(f'Logged on as {self.user}!')

@bot.event
async def on_message(self, message):
    if message.author == self.user:
        return
    translate = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&dj=1&source=input&q={message}")
    gtranslate_result = json.loads(translate.text)
    if gtranslate_result["src"] == "en":
        return
    else:
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
        # message sending will go here eventually









bot.run(token)
