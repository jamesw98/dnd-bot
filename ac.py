import os
import discord
from dotenv import load_dotenv

from parse_cmd import parse

load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

# Things todo:
# TODO implement character remove
# TODO implement character help message
# TODO implement initiative help message
# TODO consider health tracking with init tracking
#        string format()? have HP print before character name?
# TODO unit tests
# TODO github actions with unit tests

@client.event
async def on_ready():
    print("AC Started")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="D&D | '!dnd help`"))

@client.event
async def on_message(msg):
    if (msg.author == client.user):
        return

    if ("!dnd" in msg.content):
        await msg.channel.send(parse(msg))

client.run(TOKEN)