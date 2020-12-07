import os
import discord
import sys

from dotenv import load_dotenv
from parse_cmd import parse

"""
Adventurer Companion v0.05
A D&D helper bot for Discord

Thanks for taking the time to read my code :)
I mainly wrote this as a fun project in my spare time 
as well as a way to learn more about Python and how to 
write a bot for Discord. I've written a similar application
in Kotlin for Android devices, and when I decided I wanted to
learn how to write a Discord bot, I thought my D&D app 
would be a good thing to port over. 

If you'd like to take a look at the documentation, check
README.md or head to my GitHub: github.com/jamesw98/dnd-bot,
but if you are reading this, you are probably already coming
from GitHub
"""

load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

# Features to add
# TODO spellbook builder
# TODO add more things to be able to search (this should be easy, save for rainy day)

# Bugs to fix
# none visible to me :^)

# Later TODOs
# TODO github actions (unit tests)

# bot starts up
@client.event
async def on_ready():
    print("Adventure Companion Started\nHappy Adventuring!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="D&D | '!dnd help`"))

# listens to text messages for channels it has access to 
@client.event
async def on_message(msg):
    # makes sure the bot can't message itself
    if (msg.author == client.user):
        return
    # if the message has the keyword, parse the command
    # and show the user the resulting message
    if ("!dnd" in msg.content):
        result = parse(msg)

        if (type(result) == str):
            await msg.channel.send(result)
        elif (type(result) == discord.Embed):
            await msg.channel.send(embed=result)

client.run(TOKEN)