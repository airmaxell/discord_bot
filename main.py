import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import asyncio
import youtube_dl

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

# URL: https://discord.com/api/oauth2/authorize?client_id=953097989017194526&permissions=397535341654&scope=bot

# intents = discord.Intents.default()
# intents.members = True

# client = discord.Client()

client = commands.Bot(command_prefix='$')

TOKEN = "OTUzMDk3OTg5MDE3MTk0NTI2.Yi_nrA.J3hba2z1YnHPomWRMNnSoTTRAfc"

players = {}
ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdlopts)


@client.event
async def on_ready():
    print('We have logged in ad {0.user}'.format(client))


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello')


@client.event
async def on_member_join(member):
    guild = member.guild
    print(f"Guild = {guild}")
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)


@client.command(pass_context=True)
async def hello(ctx):
    await ctx.send("Hello, I'm your bot.")


@commands.command()
async def test(ctx):
    print("primio command")
    await ctx.send("Hello, this is a test from MaxinBot!")


@client.command(pass_context=True)
async def join(ctx):
    print("Join command")
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()

    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command!")


@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


@client.command(pass_context=True)
async def play(ctx, arg):

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    # if ctx.author.voice:
    #     channel = ctx.message.author.voice.channel
    #     voice = await channel.connect()

    try:
        if os.path.isfile('ytdl/song.mp3'):
            os.remove('ytdl/song.mp3')
    except:
        await ctx.send("Wait for the current song to finish.")

    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    source = FFmpegPCMAudio('maxa.mp3')
    if not arg is None:
        if arg == 'maxa':
            source = FFmpegPCMAudio('maxa.mp3')
            player = voice.play(source)
        elif arg.startswith('http'):
            with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                ydl.download([arg])
            for file in os.listdir('ytdl'):
                if file.endswith('.mp3'):
                    os.rename(os.path.join("ytdl", file),
                              os.path.join("ytdl", "song.mp3"))
            voice.play(discord.FFmpegPCMAudio("ytdl/song.mp3"))
        else:
            ctx.send("Can't play!")


@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("I'm not playing anything!")


client.add_command(test)
client.run(TOKEN)
