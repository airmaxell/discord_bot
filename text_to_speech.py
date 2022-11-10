import this
import discord
from discord.ext import commands
import random
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import youtube_dl
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from gtts import gTTS
from errors import *

class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
    
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = discord.Embed(title="", description="No channel to join. Please call `,join` from a voice channel.", color=discord.Color.green())
                await ctx.send(embed=embed)
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👍')
        await ctx.send(f'**Joined `{channel}`**')
        
    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player
    
    @client.event
    async def on_voice_state_update(member, before, after):
        print(member.voice)
        print(member.guild)
        print(member.display_name)
        if member.bot:
            print("member is a bot.")
            return
        if after.channel is not None:
            return
        
    @commands.command(name='speech', aliases=['spch','sp'], description="Speech text")
    async def play_(self, ctx, *, text_to_speech: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        if text_to_speech == "maxa":
            source = FFmpegPCMAudio('maxa.mp3')
            await player.play_static(source)
        
        elif text_to_speech == "lol":
            myobj = gTTS(text="lolovi dronovi speed bollovi", lang='sr', slow=False)
            f_name = f"tts/{ctx.message.guild}.mp3"
            myobj.save(f_name)
            await player.play_static(FFmpegPCMAudio(f_name))
        else:
            myobj = gTTS(text=text_to_speech, lang='sr', slow=False)
            f_name = f"tts/{ctx.message.guild}.mp3"
            myobj.save(f_name)
            await player.play_static(FFmpegPCMAudio(f_name))
    

