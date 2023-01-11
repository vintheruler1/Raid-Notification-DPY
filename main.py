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

bot = commands.Bot(command_prefix= commands.when_mentioned_or("!"), intents=intents, case_insensitive=True) #, intents=intents
bot.remove_command('help')

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

# A dictionary to store the number of pings/mentions for each user and role
ping_counts = defaultdict(int)

# A dictionary to store the time of the last ping/mention for each user and role
last_ping_time = defaultdict(lambda: datetime.min)

@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # Check if the message contains pings/mentions
    if message.mentions:
        # Increment the ping counts for all the users and roles that are mentioned
        for mention in message.mentions:
            ping_counts[mention.id] += 1
            last_ping_time[mention.id] = message.created_at

        # Check if any of the users or roles have been pinged/mentioned more than 6 times within 3 seconds
        for mention in message.mentions:
            if (ping_counts[mention.id] > 6 and
                    message.created_at - last_ping_time[mention.id] < timedelta(seconds=3)):
                # Send a message to the channel warning the user about excessive pinging/mentioning
                await message.channel.send("Please do not ping/mention other users or roles excessively.")
        
    await bot.process_commands(message)


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