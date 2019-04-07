import pandas as pd
import asyncio
import discord
from discord.ext import commands

TOKEN = "secrete"

client = commands.Bot(command_prefix = '!')
star_emoji = '🌟'
print(f'loaded client {star_emoji}')


async def secess():
    print("Working...")
    await client.close()
    asyncio.get_event_loop().stop()

try:
  client.loop.create_task(secess())
  client.run(TOKEN)
finally:
  asyncio.new_event_loop().run_until_complete(client.close())


'''
url="https://docs.google.com/spreadsheets/u/4/d/e/2PACX-1vSynnae4tvHp3BRCJVXVxdGizZgD8Ebq9DNTWy1NzUfWGZWXjrFKtlcO9Kz0KlcHnyMKzPck6RyEiMP/pubhtml?gid=507423927&single=true"  # Use the local copy instead.
table = pd.read_html(url,header=1)[0]
table = table.dropna(axis=0, how='any')
print(table)
'''
