import os
import discord
import requests
import json
intents = discord.Intents.default()
intents.message_content = True
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user:
            return
        translate = requests.get(f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&dj=1&source=input&q={message}")
        gtranslate_result = json.loads(translate.text)
        if gtranslate_result["src"] == "en":
            return
        else:
            #data = {
            #    "text": message,
            #    "source_lang": gtranslate_result["src"].upper(),
            #   "target_lang": "EN-US"
            #
            #}
            sentences = gtranslate_result['sentences']
            sentences_json = sentences[0]
            final_sentence = sentences_json['trans']








client = MyClient(intents=intents)
client.run(token)
