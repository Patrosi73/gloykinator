# gloykinator
a very shitty discord automatic translation bot

![image](https://github.com/user-attachments/assets/384fd7bd-d067-4c35-8fc6-7e4972fde143)

# setup
- create a bot and invite to server
  - make sure that the bot has **guilds**, **messages** and **message content intents**
  - make sure that the bot has **manage webhooks** and **manage messages** permissions
- get bot token, create a `.env` file in the same directory with the contents `TOKEN=` appending your discord bot's token
- run the bot

# deepl support (via DeeplX)
> [!IMPORTANT]
> this is very unstable and will likely hit a rate-limit after just a few translated messages in a short span of time.
> 
> if a rate-limit is encountered the bot will fall back to google translate.
> 
> official api support maybe sometime in the future

> [!NOTE]
> this will still send messages to Google for source language detection as the deepl one is very spotty.
> 
> nothing i can do about that unfortunately :(

## setup
- i recommend hosting a deeplx api endpoint locally. as of writing this, only [deeplx-python](https://github.com/cnbeining/DeepLX-Python) seems to currently work
- add these two lines to your `.env` file:
  ```
  USE_DEEPLX=1
  DEEPLX_API="http://127.0.0.1:8000/translate"
  ```
- if the server is reachable it should attempt translating the message through deepl!
