import sys
from discord.ext import commands
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
import os

token = str(sys.argv[1]) # the first argument passed to the script should be the bot token
bot = commands.Bot(command_prefix='/') # all commands should start with '/'

# command list
command_list = ['play', 'disconnect', 'pause', 'resume', 'stop']

# command abbreviations
play_abbrs = ['p']
disconnect_abbrs = ['dc', 'leave', 'l']
pause_abbrs = ['pp', 'ps']
resume_abbrs = ['r', 'rs']
stop_abbrs = ['s']

@bot.command()
async def play(ctx, arg):
    await joinChannel(ctx)
    downloadMusic(arg)
    await playMusic(ctx)

@bot.command()
async def disconnect(ctx):
    await leaveChannel(ctx)

@bot.command()
async def pause(ctx):
    await pauseMusic(ctx)

@bot.command()
async def resume(ctx):
    await resumeMusic(ctx)

@bot.command()
async def stop(ctx):
    await stopMusic(ctx)  

async def joinChannel(ctx):
    if ctx.author.voice: # user is in voice channel
        channel = ctx.author.voice.channel
        if not bot.voice_clients: # bot is not already in voice channel
            await channel.connect()
        elif bot.voice_clients[0].channel != channel: # bot is not already in same voice channel
            await bot.voice_clients[0].disconnect()
            await channel.connect()
    else:
        await ctx.send('Join a voice channel first.')

async def leaveChannel(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()

async def playMusic(ctx):
    if not bot.voice_clients: # bot is not connected to voice channel
        return

    vc = ctx.guild.voice_client
    audio = FFmpegPCMAudio('song.mp3')
    if not vc.is_playing():
        vc.play(audio)

async def pauseMusic(ctx):
    vc = ctx.guild.voice_client
    if vc.is_playing():
        vc.pause()
    else:
        await ctx.send('There is no music playing right now.')

async def resumeMusic(ctx):
    vc = ctx.guild.voice_client
    if vc.is_paused():
        vc.resume()
    else:
        await ctx.send('There is no music paused right now.')

async def stopMusic(ctx):
    vc = ctx.guild.voice_client
    vc.stop()

def downloadMusic(url):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }

    with YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.replace(file, "song.mp3")
            break

# Check for and expand any abbreviated commands
async def expandAbbrCommand(message):
    message.content += ' '
    abbrs = combineAbbrs()
    for abbr in abbrs:
        command = command_list[abbrs[abbr]]
        if message.content.startswith(f"/{abbr} "):
            message.content = message.content.replace(f"/{abbr} ", f"/{command} ", 1)
            break 

# Combines all the abbreviated commands into one dictionary
# The key is the abbreviation, the value is the index pointing to the command
# (in the 'command_list' list)
def combineAbbrs():
    abbrs = {}
    for i, c in enumerate(command_list):
        for abbr in globals()[f'{c}_abbrs']:
            abbrs[abbr] = i
    return abbrs

async def on_message(self, message):
    await expandAbbrCommand(message)
    await self.process_commands(message)
commands.Bot.on_message = on_message

bot.run(token)
