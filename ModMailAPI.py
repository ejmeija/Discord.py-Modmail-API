import discord
from discord import app_commands
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)
# Global Vars
settings = {}
with open("settings.txt", "r") as f:
    lines = f.read().splitlines()
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            settings[key] = value
    if "modmail_user_id" in settings:
        settings["modmail_user_id"] = int(settings["modmail_user_id"])
    # Convert all other settings to strings
    for key in settings:
        if key != "modmail_user_id":
            settings[key] = str(settings[key])

#Main & Sending Messages
class MainBody():
    def __init__(self, client):
        self.client = client
        self.tree = app_commands.CommandTree(client)
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        print("Presence is set to: " + settings["presence"])
        print('(Thanks for adding MODMAIL API! Created and maintained by e.the.insane)')
        await client.change_presence(activity=discord.Game(name=settings["presence"]))
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if not message.guild:
            if message.author.id == settings["modmail_user_id"]:
                return
            modmail_user = client.get_user(settings["modmail_user_id"])
            if modmail_user:
                await modmail_user.send(f"**{message.author}**: {message.content}")

if settings["token"] == "your_token_here":
    print("Please set your token in settings.txt")
else:
    main_body = MainBody(client)
    client.run(settings["token"])