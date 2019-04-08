import pandas as pd
import asyncio
import discord
from discord.ext import commands
from itertools import cycle
import os


import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secrete.json',scope)
sheet_client = gspread.authorize(creds)

sheet = sheet_client.open('Project Creation - Flux Federal Campaign (Responses)').sheet1
contents = sheet.get_all_records()

print(contents[1]['Completion Date'])
print("Ok")



TOKEN = os.environ.get('FM_DISCORD_BOT_TOKEN', None)

DISCORD_CHANNEL = "551999201714634757"

client = commands.Bot(command_prefix = '!')

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
