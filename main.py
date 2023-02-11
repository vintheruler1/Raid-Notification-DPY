import nextcord
import asyncio
from nextcord import *
import datetime
from nextcord.ext import commands

# Initialize the bot object
#Bot Defining Stuff
intents = nextcord.Intents.default()

intents.members = True
intents.presences = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix= commands.when_mentioned_or("!"), intents=intents, case_insensitive=True) #, intents=intents
bot.remove_command('help')

servers = [1060354348678402179]

# A dictionary to store the count of pings for each user
ping_count = {}

# A list to store the timestamp of the last ping for each user
last_ping = {}

#role_ping_count = {}
#role_last_ping = {}

mainChannel = 1073762906400886824

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
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.mentions:
        # Get the user who sent the message
        user = message.author
        
        # Get the current timestamp
        now = message.created_at
        
        # If this is the first time the user is pinging, initialize the count and last ping timestamp
        if user not in ping_count:
            ping_count[user] = 1
            last_ping[user] = now
        
        # If the user has pinged before
        else:
            # Check the time difference between the last ping and the current ping
            time_diff = (now - last_ping[user]).total_seconds()
            
            # If the time difference is less than 3 seconds
            if time_diff < 3:
                # Increment the ping count
                ping_count[user] += 1
                
                # If the ping count is 6 or more
                if ping_count[user] >= 6:
                    # Send a message to the channel to warn the user
                    try:
                        for c in message.guild.channels:
                            if c.permissions_for(guild.me).create_instant_invite:
                                invite = await c.create_invite()
                                break
                    except:
                        invite = "No-Invite-Found"
                    try:
                        emergency_ping_role = nextcord.utils.get(message.guild.roles, name='emergencyPing').id
                    except:
                        emergency_ping_role = "No Emergency Role Found"
                    embed = nextcord.Embed(
                        title=f"{message.author} was caught attempting to raid.",
                        description = f"{message.author} / {message.author.id} / {message.author.mention} was caught attempting to raid. They were **timed out for 1 day.**",
                    )
                    duration = datetime.timedelta(minutes=1440)
                    await message.channel.send(f'<@&{emergency_ping_role}> was caught spam pinging.', embed=embed)
                    await message.author.edit(timeout=duration, reason="Caught spam pinging/spam pinging a role. Timed out for 1 day")
                    channel = bot.get_channel(int(mainChannel))
                    embed = nextcord.Embed(
                        title=f"{message.author} was caught attempting to raid in ({message.guild.name})[{invite}].", # get a invite to the server
                    )
                    
                    
                    # Reset the ping count
                    ping_count[user] = 0
                    
            # If the time difference is 3 seconds or more
            else:
                # Reset the ping count
                ping_count[user] = 1
                
            # Update the last ping timestamp
            last_ping[user] = now
            
    if message.role_mentions:
        user = message.author
        now = message.created_at
        
        if user not in ping_count:
            ping_count[user] = 1
            last_ping[user] = now
        
        else:
            time_diff = (now - last_ping[user]).total_seconds()
            
            if time_diff < 3:
                ping_count[user] += 1
                
                if ping_count[user] >= 6:
                    try:
                        for c in message.guild.channels:
                            if c.permissions_for(guild.me).create_instant_invite:
                                invite = await c.create_invite()
                                break
                    except:
                        invite = "No-Invite-Found"
                    try:
                        emergency_ping_role = nextcord.utils.get(message.guild.roles, name='emergencyPing').id
                    except:
                        emergency_ping_role = "No Emergency Role Found"
                    embed = nextcord.Embed(
                        title=f"{message.author} was caught attempting to raid.",
                        description = f"{message.author} / {message.author.id} / {message.author.mention} was caught attempting to raid. They were **timed out for 1 day.**",
                    )
                    duration = datetime.timedelta(minutes=1440)
                    await message.channel.send(f'<@&{emergency_ping_role}> was caught spam pinging.', embed=embed)
                    await message.author.edit(timeout=duration, reason="Caught spam pinging/spam pinging a role. Timed out for 1 day")
                    channel = bot.get_channel(int(mainChannel))
                    embed = nextcord.Embed(
                        title=f"{message.author} was caught attempting to raid in ({message.guild.name})[{invite}].", # get a invite to the server
                    )
                    await channel.send("Warning! A possible raid has been found.", embed = embed)
                    ping_count[user] = 0
                    
            else:
                ping_count[user] = 1
                
            last_ping[user] = now
            
    await bot.process_commands(message)

@bot.command()
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

@bot.command(pass_context=True, aliases=['purge', "clear"])
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

# @bot.slash_command(guild_ids=[servers], description="Create the role 'emergencyPing' which will be pinged if the bot detects a raid.")
# async def createRole(interaction : Interaction):
#     guild = interaction.guild
#     role = nextcord.utils.get(guild.roles, name='emergencyPing')
#     if not role:
#         role = await guild.create_role(name='emergencyPing',
#                                        color=nextcord.Color.red(),
#                                        mentionable=False)
#         await interaction.send(f'The role "emergencyPing" has been created. Rank this to users who should be notified if this bot detects if there is a raid.')
#     else:
#         await interaction.send('The role "emergencyPing" already exists.')

import os
#Running the Bot!
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)