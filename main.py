#!/usr/bin/env python3
import os
import discord
import sys
import traceback

from dotenv import load_dotenv
from parse_cmd import parse

load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

# Features to add
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