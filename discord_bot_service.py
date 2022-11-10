import random
from pathlib import Path
from smwin_service import SMWinservice
from discord.ext import commands

from music_player import Music


class DiscordBot(SMWinservice):
    _svc_name_ = "DiscordBotService"
    _svc_display_name_ = "Discord bot service"
    _svc_description_ = "Service that runs discord bot in background"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        with open('I:\\code\\discord_bot\\demo.txt', 'a') as sourceFile:
            print('Main called', file = sourceFile)
        client = commands.Bot(command_prefix='$')
        client.add_cog(Music(client)) 

        @client.event
        async def on_ready():
            print('We have logged in ad {0.user}'.format(client))
        
        TOKEN = "OTUzMDk3OTg5MDE3MTk0NTI2.Yi_nrA.ilQPHYeSePnHHRHbI4HXUBj85Zw"
        client.run(TOKEN)