from discord.ext import commands
import discord

from music_player import Music


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)
client.add_cog(Music(client)) 
# setup(client)

@client.event
async def on_ready():
    print('We have logged in ad {0.user}'.format(client))

TOKEN = "OTUzMDk3OTg5MDE3MTk0NTI2.GA8pnl.YZke2tlON1HDO7Bgi0kiVL2FaJUzTkSBzbpZSo"
client.run(TOKEN)