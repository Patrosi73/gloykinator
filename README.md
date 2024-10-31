# gloykinator
a very shitty discord automatic translation bot

![image](https://github.com/user-attachments/assets/384fd7bd-d067-4c35-8fc6-7e4972fde143)

# setup
- create a bot and invite to server
  - make sure that the bot has **guilds**, **messages** and **message content intents**
  - make sure that the bot has **manage webhooks** and **manage messages** permissions
- to make it nicer, make sure that there's one webhook created for **every channel**. otherwise the bot will yell at you!
  - add `IGNORE_NOWEBHOOK=1` to .env to disable the warning
- get bot token, create a `.env` file in the same directory with the contents `TOKEN=` appending your discord bot's token
- run the bot
