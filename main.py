import pandas as pd
import asyncio
import discord
from discord.ext import commands
from itertools import cycle
import os

TOKEN = os.environ.get('FM_DISCORD_BOT_TOKEN', None)

DISCORD_CHANNEL = "551999201714634757"

client = commands.Bot(command_prefix = '!')
star_emoji = '🌟'
print(f'loaded client {star_emoji}')


async def displayembed():
    await client.wait_until_ready()
    embed = discord.Embed(
    title = "New Project",
    description = "This is the description",
    colour = discord.Colour.blue()
    )
    embed.set_footer(text = "This is a footer")
    await client.send_message(discord.Object(DISCORD_CHANNEL), embed = embed)
    await client.close()
    asyncio.get_event_loop().stop()

try:
    client.loop.create_task(displayembed())
    client.run(TOKEN)
finally:
    asyncio.new_event_loop().run_until_complete(client.close())


'''
url="https://docs.google.com/spreadsheets/u/4/d/e/2PACX-1vSynnae4tvHp3BRCJVXVxdGizZgD8Ebq9DNTWy1NzUfWGZWXjrFKtlcO9Kz0KlcHnyMKzPck6RyEiMP/pubhtml?gid=507423927&single=true"  # Use the local copy instead.
table = pd.read_html(url,header=1)[0]
table = table.dropna(axis=0, how='any')
print(table)
'''
