
import sys
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from yt_dlp import YoutubeDL
import os
from youtube_search import YoutubeSearch
import re
import asyncio

bot = commands.Bot(command_prefix='/') # all commands should start with '/'

# all possible commands and their abbreviations
command_list = ['play', 'disconnect', 'pause', 'resume', 'stop', 'now_playing', 'queue', 'skip', 'move']
play_abbrs = ['p']
disconnect_abbrs = ['dc', 'leave', 'l']
pause_abbrs = ['pp', 'ps']
resume_abbrs = ['r', 'rs']
stop_abbrs = ['st']
now_playing_abbrs = ['np']
queue_abbrs = ['q']
skip_abbrs = ['sk', 'pskip', 'play_skip']
move_abbrs = ['mv', 'm']

# keep track of the songs to play next
song_queue = []
current_song = ""
stopped = False

@bot.command()
async def play(ctx, *, arg):
    await joinChannel(ctx)
    if not bot.voice_clients: # bot is not connected to voice channel
        return

    song_id, song_title = await get_song_info(arg)

    #print(song_id, "\n", song_title)
    if not ctx.voice_client.is_playing(): # bot is not playing music yet
        await playMusic(ctx, song_id, song_title)
        global stopped
        stopped = False
    else: # bot is already playing music, so just queue the song
        song_queue.append((song_id, song_title))
        await ctx.send(f"**added to queue:** {song_title}")

@bot.command()
async def disconnect(ctx):
    await stop(ctx)
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()

@bot.command()
async def pause(ctx):
    vc = ctx.guild.voice_client
    if vc.is_playing():
        vc.pause()

@bot.command()
async def resume(ctx):
    vc = ctx.guild.voice_client
    if vc.is_paused():
        vc.resume()

@bot.command()
async def stop(ctx):
    if not bot.voice_clients: # bot is not connected to voice channel
        return

    global stopped
    stopped = True
    vc = ctx.guild.voice_client
    vc.stop()

@bot.command()
async def now_playing(ctx):
    await ctx.send(f"**__Now Playing:__** {current_song}")

@bot.command()
async def queue(ctx):
    if song_queue:
        queue_msg = "**Song Queue:**\n"
        for place, (_, song_title) in enumerate(song_queue):
            queue_msg += f'**[{place}]** {song_title}\n'
        await ctx.send(queue_msg)
    else:
        await ctx.send("Song queue is empty.")

@bot.command()
async def skip(ctx, *args):
    if len(args):
        await stop(ctx)
        await play(ctx=ctx, arg=''.join(list(args)))
    else:
        await stop(ctx)
        if song_queue:
            song_id, song_title = song_queue.pop(0)
            await playMusic(ctx, song_id, song_title)

@bot.command()
async def move(ctx, q_pos_src, q_pos_dst):
    q_pos_src = int(q_pos_src)
    q_pos_dst = int(q_pos_dst)
    if q_pos_src < len(song_queue) and q_pos_dst < len(song_queue) and q_pos_src >= 0 and q_pos_dst >= 0 and q_pos_src != q_pos_dst: # sanitize input
        song_id, song_title = song_queue.pop(q_pos_src)
        song_queue.insert(q_pos_dst, (song_id, song_title))
        await ctx.send(f"**moved song to position {q_pos_dst}:** {song_title}")

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

async def get_song_info(arg):
    arg = str(arg)
    if arg.startswith(r"https://"): # url link
        song_url = arg
    else: # search term
        search_results = YoutubeSearch(str(arg), max_results=1).to_dict()
        song_url = r"https://youtu.be" + search_results[0]["url_suffix"]

    song_id, song_title = downloadMusic(song_url)
    return song_id, song_title

async def play_next_song(ctx):
    if song_queue and not stopped:
        next_song_id, next_song_title = song_queue.pop(0)
        await playMusic(ctx, next_song_id, next_song_title)

async def playMusic(ctx, video_id, video_title):
    vc = ctx.guild.voice_client    
    if not vc.is_playing():
        audio = FFmpegPCMAudio(rf'songs/{video_id}.mp3')
        # play the current song then play the next one in queue after it finishes
        vc.play(audio, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop))
        vc.source = PCMVolumeTransformer(vc.source, volume=0.25)
        global current_song
        current_song = video_title
        await now_playing(ctx)

def downloadMusic(url):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
    }

    with YoutubeDL(ytdl_opts) as ytdl: # works with SC links too apparently 
        ytdl.download([url])

    if not os.path.exists("songs"):
        os.makedirs("songs")

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            song_id = re.findall(r"(?<=\[).+?(?=\])", file)[-1]
            song_title = file[:-(len(f" [{song_id}].mp3"))]
            os.replace(file, rf"songs/{song_id}.mp3")

    return song_id, song_title

# Combines all the abbreviated commands into one dictionary
# The key is the abbreviation, the value is the index pointing to the command
# (in the 'command_list' list)
def combineAbbrs():
    abbrs = {}
    for i, c in enumerate(command_list):
        for abbr in globals()[f'{c}_abbrs']:
            abbrs[abbr] = i
    return abbrs

# Check for and expand any abbreviated commands
async def expandAbbrCommand(message):
    message.content += ' '
    abbrs = combineAbbrs()
    for abbr in abbrs:
        command = command_list[abbrs[abbr]]
        if message.content.startswith(f"/{abbr} "):
            message.content = message.content.replace(f"/{abbr} ", f"/{command} ", 1)
            break 

async def on_message(self, message):
    await expandAbbrCommand(message)
    await self.process_commands(message)
commands.Bot.on_message = on_message

def main():
    token = str(sys.argv[1]) # the first argument passed to the script should be the bot token
    bot.run(token)

if __name__ == '__main__':
    main()
