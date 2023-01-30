#Imports
import nextcord
from nextcord import *
from nextcord.ext import commands

import os

############################################################################################
############################################################################################
############################################################################################


#Bot Defining Stuff
intents = nextcord.Intents.default()

intents.members = True
intents.presences = True
intents.messages = True
intents.message_content = True

servers = []
mainChannel = 12345

bot = commands.Bot(command_prefix= commands.when_mentioned_or("!"), intents=intents, case_insensitive=True) #, intents=intents
bot.remove_command('help')

import asyncio

@bot.event
async def on_message(message):
    if message.mentions:
        mentions = [user for user in message.mentions if not user.bot]
        if len(mentions) >= 6:
            invite = await guild.create_invite(max_uses=100, temporary=True)
            emergency_ping_role = nextcord.utils.get(message.guild.roles, name='emergencyPing')
            embed = nextcord.Embed(
                title=f"{message.author} was caught attempting to raid.",
                description = f"{message.author} / {message.author.id} / {message.author.mention} was caught attempting to raid. They were timed out for 1 day.",
            )
            await message.channel.send(f'<&{emergency_ping_role}> was caught spam pinging.', embed=embed)
            await message.author.edit(timeout=86400, reason="Caught spam pinging/spam pinging a role. Timed out for 1 day")
            channel = bot.get_channel(id=int(mainChannel))
            embed = nextcord.Embed(
                title=f"{message.author} was caught attempting to raid in ({message.guild.name})[{invite}].", # get a invite to the server
            )
            
    await bot.process_commands(message)


@client.command()
async def createRole(ctx):
    guild = ctx.guild
    role = nextcord.utils.get(guild.roles, name='emergencyPing')
    if not role:
        role = await guild.create_role(name='emergencyPing',
                                       color=nextcord.Color.red(),
                                       mentionable=False)
        await ctx.reply(f'The role "emergencyPing" has been created. Rank this to users who should be notified if this bot detects if there is a raid.')
    else:
        await ctx.reply('The role "emergencyPing" already exists.')

@bot.slash_command(guild_ids=[servers], description="Create the role 'emergencyPing' which will be pinged if the bot detects a raid.")
async def createRole(interaction : Interaction):
    guild = interaction.guild
    role = nextcord.utils.get(guild.roles, name='emergencyPing')
    if not role:
        role = await guild.create_role(name='emergencyPing',
                                       color=nextcord.Color.red(),
                                       mentionable=False)
        await interaction.send(f'The role "emergencyPing" has been created. Rank this to users who should be notified if this bot detects if there is a raid.')
    else:
        await interaction.send('The role "emergencyPing" already exists.')



@bot.event
async def on_guild_join(guild):
    # Add the server ID to the list
    servers.append(guild.id)

#create an @bot.event to detect a mass pinging / mass raiding of some sort 


@bot.event
async def on_connect():
    print('connected')
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="for raids."), status=nextcord.Status.online)

@bot.event
async def on_ready():
    print('ready')
    

#Running the Bot!
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)