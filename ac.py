import os
import discord
from dotenv import load_dotenv

from parse_cmd import parse

load_dotenv()

TOKEN = os.getenv('TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print("AC Started")

@client.event
async def on_message(msg):
    if (msg.author == client.user):
        return

    if ("!dnd" in msg.content):
        await msg.channel.send(parse(msg))

client.run(TOKEN)