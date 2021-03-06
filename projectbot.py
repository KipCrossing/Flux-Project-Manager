import asyncio
import discord
from discord.ext import commands
from itertools import cycle
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secrete.json', scope)
sheet_client = gspread.authorize(creds)
sheet = sheet_client.open('Project Data').sheet1
contents = sheet.get_all_records()

TOKEN = os.environ.get('FM_DISCORD_BOT_TOKEN', None)

DISCORD_CHANNEL = 562897002107764736
ERROR_CHANNEL = 562605716591083560

client = commands.Bot(command_prefix='!')

client.remove_command('help')

resorce_contact = {
    'Funding': '555985616416931841',
    'Social Media': '313952769541406720',
    'Campaign Materials': '565085841223974912',
    'Permissions': '199731686093619200',
    'Other Volunteers': '',
    'Nothing': ''
}


channel_dict = {
    'Enhance General Awareness': '563627640582569984',
    'Empower Volunteers to Action': '563628133215895576',
    'Boost Active Membership': '563628133215895576',
    'Develop Candidate Pipeline': '561468141625016322',
    'Document & Codify Our Processes': '563942886685802526'
}

colour_dict = {
    'Enhance General Awareness': discord.Colour.red(),
    'Empower Volunteers to Action': discord.Colour.green(),
    'Boost Active Membership': discord.Colour.purple(),
    'Develop Candidate Pipeline': discord.Colour.orange(),
    'Document & Codify Our Processes': discord.Colour.blue(),
    'Launch Tech': discord.Colour.blue(),
    'Team & Organization Building': discord.Colour.green(),
    'Scaling Membership': discord.Colour.purple(),
    'Prepare Candidates': discord.Colour.red()
}


@client.command(pass_context=True)
async def help(ctx, *args):
    channel = ctx.message.channel
    descrip = '**!project `[num]`** - Displays the project with assigned number'
    descrip += '\n**!active** - Shows all active projects'
    embed = discord.Embed(
        title='Commands list:',
        description=descrip,
        colour=discord.Colour.red()
    )
    await channel.send(embed=embed)


@client.command(pass_context=True)
async def active(ctx, *args):
    channel = ctx.message.channel
    error_channel = client.get_channel(ERROR_CHANNEL)
    try:
        rown = 0
        for row in contents:
            if row['Status'] == 'Active':
                print(rown)
                await channel.send(embed=make_embed(contents[rown], str(rown+2)))
            rown += 1
    except Exception as e:
        print(f'Got exception: {str(e)}')
        await channel.send('Bad command :(')
        await error_channel.send(str(e))


@client.command(pass_context=True)
async def project(ctx, *args):
    channel = ctx.message.channel
    error_channel = client.get_channel(ERROR_CHANNEL)
    try:
        if len(args) == 1:
            if int(args[0]) > 1:
                if contents[int(args[0])-2]['Discord'] != '':
                    rown = int(args[0])-2
                    await channel.send(embed=make_embed(contents[rown], str(args[0])))
    except Exception as e:
        print(f'Got exception: {str(e)}')
        await channel.send('Bad command :(')
        await error_channel.send(str(e))


def make_embed(project_info, project_num):
    embed = discord.Embed(
        title=project_info['Project Nickname'] + '\n' + project_info['Project Subtitle'],
        description=project_info['Description of Project'],
        colour=colour_dict[project_info['Key Objective']]
    )
    embed.set_footer(text=project_info['Key Objective'])
    embed.set_author(name=project_info['Volunteer name'])
    embed.add_field(name='Resource', value=project_info['Resources Needed '])
    embed.add_field(name='Description of Resources',
                    value=project_info['Description of Resources Needed'])
    embed.add_field(name='Project Number', value=project_num)
    embed.add_field(name='Expected outcomes', value=project_info['Expected outcomes'])
    embed.add_field(name='Completion Date', value=project_info['Completion Date'])
    return embed


async def check_sheet():
    posted_list = []
    await client.wait_until_ready()
    print('Ready!')
    channel = client.get_channel(DISCORD_CHANNEL)
    error_channel = client.get_channel(ERROR_CHANNEL)

    while not client.is_closed():
        print("YES")
        try:
            rown = 1
            for row in contents:
                rown += 1
                if row['Discord'] == '' and not rown in posted_list:
                    resorces_list = row['Resources Needed '].split(", ")
                    print(resorces_list)
                    # for res in resorces_list:
                    #     if resorce_contact[res] != '':
                    #         user = await client.get_user_info(resorce_contact[res])
                    #         # await client.send_message(user, "A new project is requesting resources that may require your attention.\
                    #         #  \nPlease see the project channel\
                    #         #  \n**Project Name:** " +str(row['Project Nickname']))

                    Embed = make_embed(row, rown)
                    await channel.send(embed=Embed)

                    message = 'Please read the above project and ask to collaborate if you are interested.'
                    await channel.send(message)

                    sheet.update_cell(rown, 11, str(rown))
                    posted_list.append(rown)
                    print(row['Project Nickname'])
            await asyncio.sleep(60)
        except Exception as e:
            print(f'Got exception: {str(e)}')
            await error_channel.send(str(e))


try:
    client.loop.create_task(check_sheet())
    client.run(TOKEN)
finally:
    # asyncio.new_event_loop().run_until_complete(client.close())
    print('fin')
