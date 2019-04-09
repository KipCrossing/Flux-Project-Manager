import pandas as pd
import asyncio
import discord
from discord.ext import commands
from itertools import cycle
import os


import gspread
from oauth2client.service_account import ServiceAccountCredentials



TOKEN = os.environ.get('FM_DISCORD_BOT_TOKEN', None)

DISCORD_CHANNEL = "559620454847873024"

client = commands.Bot(command_prefix = '!')

colour_dict = {
'Enhance General Awareness': discord.Colour.red(),
'Empower Volunteers to Action': discord.Colour.green(),
'Boost Active Membership' : discord.Colour.purple(),
'Develop Candidate Pipeline' : discord.Colour.orange(),
'Document & Codify Our Processes' : discord.Colour.blue()
}

async def displayembed(p_title,desc,footer,v_name,resorce,resorce_desc,date):
    await client.wait_until_ready()
    embed = discord.Embed(
    title = p_title,
    description = desc,
    colour = colour_dict[footer]
    )
    embed.set_footer(text = footer)
    embed.set_author(name = v_name)
    embed.add_field(name = 'Resource',value = resorce)
    embed.add_field(name = 'Description of Resources',value = resorce_desc)
    embed.add_field(name = 'Completion Date',value = date)
    await client.send_message(discord.Object(DISCORD_CHANNEL), embed = embed)
    #await client.send_message(discord.Object(DISCORD_CHANNEL), "**Project Description**:\n"desc)
    await client.close()
    asyncio.get_event_loop().stop()


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secrete.json',scope)
sheet_client = gspread.authorize(creds)

sheet = sheet_client.open('Project Creation').sheet1
contents = sheet.get_all_records()


rown = 1
for row in contents:
    rown+=1
    if row['Discord'] == '':
        print(row)
        sheet.update_cell(rown,9,'Posted')
        print(row['Project Title'])

        try:
            client.loop.create_task(displayembed(
            row['Project Title'],
            row['Description of Project'],
            row['Key Objective'],
            row['Volunteer name'],
            row['Resources Needed '],
            row['Description of Resources Needed'],
            row['Completion Date']
            ))
            client.run(TOKEN)
        finally:
            asyncio.new_event_loop().run_until_complete(client.close())
        break
