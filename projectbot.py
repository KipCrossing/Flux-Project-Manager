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
sheet = sheet_client.open('Project Data').sheet1
contents = sheet.get_all_records()


TOKEN = os.environ.get('FM_DISCORD_BOT_TOKEN', None)

DISCORD_CHANNEL = "565421685101035530"
ERROR_CHANNEL = "562605716591083560"

client = commands.Bot(command_prefix = '!')


channel_dict = {
'Enhance General Awareness': '563627640582569984',
'Empower Volunteers to Action': '563628133215895576',
'Boost Active Membership' : '563628133215895576',
'Develop Candidate Pipeline' : '561468141625016322',
'Document & Codify Our Processes' : '563942886685802526'
}

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
            if int(args[0]) > 1:
                if contents[int(args[0])-2]['Discord'] != '':
                    rown = int(args[0])-2
                    await client.say(embed = make_embed(contents[rown],str(args[0])))
    except Exception as e:
        print(f'Got exception: {str(e)}')
        await client.say('Bad command :(')
        await client.send_message(discord.Object(ERROR_CHANNEL), str(e))

def make_embed(project_info, project_num):
    embed = discord.Embed(
    title = project_info['Project Nickname'] + '\n' + project_info['Project Subtitle'] ,
    description = project_info['Description of Project'],
    colour = colour_dict[project_info['Key Objective']]
    )
    embed.set_footer(text = project_info['Key Objective'])
    embed.set_author(name = project_info['Volunteer name'])
    embed.add_field(name = 'Resource',value = project_info['Resources Needed '])
    embed.add_field(name = 'Description of Resources',value = project_info['Description of Resources Needed'])
    embed.add_field(name = 'Project Number',value = project_num)
    embed.add_field(name = 'Expected outcomes',value = project_info['Expected outcomes'])
    embed.add_field(name = 'Completion Date',value = project_info['Completion Date'])
    return embed




async def check_sheet():
    posted_list = []
    await client.wait_until_ready()
    await client.remove_command('help')
    print('Ready!')
    while not client.is_closed:
        try:
            rown = 1
            for row in contents:
                rown+=1
                if row['Discord'] == '' and not rown in posted_list:
                    Embed = make_embed(row,rown)
                    await client.send_message(discord.Object(DISCORD_CHANNEL), embed =Embed)
                    await client.send_message(discord.Object(channel_dict[row['Key Objective']]),embed =Embed)
                    message = 'Please read the above project and ask to collaborate if you are interested. \n'
                    message2 = 'The project can also be found at: <https://trello.com/b/FM1sZEI7/volunteer-initiative-projects>'
                    await client.send_message(discord.Object(channel_dict[row['Key Objective']]),message + message2)
                    sheet.update_cell(rown,11,str(rown))
                    posted_list.append(rown)
                    print(row['Project Nickname'])
            await asyncio.sleep(60)
        except Exception as e:
            print(f'Got exception: {str(e)}')
            await client.send_message(discord.Object(ERROR_CHANNEL), e)



try:
    client.loop.create_task(check_sheet())
    client.run(TOKEN)
finally:
    asyncio.new_event_loop().run_until_complete(client.close())
