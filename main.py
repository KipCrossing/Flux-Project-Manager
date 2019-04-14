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




TOKEN = os.environ.get('FM_DISCORD_BOT_TOKEN', None)

DISCORD_CHANNEL = "565421685101035530"

client = commands.Bot(command_prefix = '!')

colour_dict = {
'Enhance General Awareness': discord.Colour.red(),
'Empower Volunteers to Action': discord.Colour.green(),
'Boost Active Membership' : discord.Colour.purple(),
'Develop Candidate Pipeline' : discord.Colour.orange(),
'Document & Codify Our Processes' : discord.Colour.blue()
}

@client.command()
async def project(*args):
    try:
        if len(args) == 1:
            if int(args[0]) > 0:
                sheet = sheet_client.open('Project Creation').sheet1
                contents = sheet.get_all_records()
                if contents[int(args[0])]['Discord'] != '':
                    rown = int(args[0])-1

                    await client.say(embed = make_embed(contents[rown],rown+1))
    except Exception as e:
        print(f'Got exception: {str(e)}')
        await client.say('Bad command :(')

def make_embed(project_info, project_num):
    embed = discord.Embed(
    title = project_info['Project Title'],
    description = project_info['Description of Project'],
    colour = colour_dict[project_info['Key Objective']]
    )
    embed.set_footer(text = project_info['Key Objective'])
    embed.set_author(name = project_info['Volunteer name'])
    embed.add_field(name = 'Resource',value = project_info['Resources Needed '])
    embed.add_field(name = 'Description of Resources',value = project_info['Description of Resources Needed'])
    embed.add_field(name = 'Completion Date',value = project_info['Completion Date'])
    embed.add_field(name = 'Project Number',value = project_num)
    return embed









async def check_sheet():
    await client.wait_until_ready()
    print('Ready!')
    while not client.is_closed:
        try:
            sheet = sheet_client.open('Project Creation').sheet1
            contents = sheet.get_all_records()
            rown = 1
            for row in contents:
                rown+=1
                if row['Discord'] == '':
                    await client.send_message(discord.Object(DISCORD_CHANNEL), embed = make_embed(row,rown))
                    print(row)
                    sheet.update_cell(rown,9,'Posted')
                    print(row['Project Title'])
            await asyncio.sleep(60)
        except Exception as e:
            print(f'Got exception: {str(e)}')



try:
    client.loop.create_task(check_sheet())
    client.run(TOKEN)
finally:
    asyncio.new_event_loop().run_until_complete(client.close())
