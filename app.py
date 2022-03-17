from discord.ext import commands

from music_player import Music


def setup(bot):
    bot.add_cog(Music(bot)) 

client = commands.Bot(command_prefix='$')

setup(client)

@client.event
async def on_ready():
    print('We have logged in ad {0.user}'.format(client))


TOKEN = "OTUzMDk3OTg5MDE3MTk0NTI2.Yi_nrA.J3hba2z1YnHPomWRMNnSoTTRAfc"
client.run(TOKEN)