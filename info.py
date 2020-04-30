import discord
import sys, os
import ast
import time
from datetime import datetime
TOKEN = 'Njk5OTY3NzM1NTM4Mzg0OTg3.XpcFyQ.e7_bFu3pi2qXbo9gDyD5TkHGBZI'

client = discord.Client()
channels = []


@client.event
async def on_ready():
    print(client.get_user(496299665227120642).avatar_url)


client.run(TOKEN)
