import sys
import os
import re
import asyncio
import urllib
import ast

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer, Color
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch, Video, ResultMode
from pretty_help import PrettyHelp, DefaultMenu


# Load command prefix from .config file
with open('source\.config', 'r') as file:
    config = file.readlines()
command_prefix = config[0][0]
#command_prefix = '/' 

ending_note = "Check the github for a list of all the commands and their descriptions:\nhttps://github.com/MrYo531/music-bot"
help_command = PrettyHelp(color=Color.blue(), ending_note=ending_note, index_title='Commands')
menu = DefaultMenu(delete_after_timeout=True)
bot = commands.Bot(command_prefix=command_prefix, help_command=help_command, menu=menu)


# Load command abbreviations from .config file
play_abbrs = ast.literal_eval(config[1])
disconnect_abbrs = ast.literal_eval(config[2])
pause_abbrs = ast.literal_eval(config[3])
resume_abbrs = ast.literal_eval(config[4])
stop_abbrs = ast.literal_eval(config[5])
now_playing_abbrs = ast.literal_eval(config[6])
queue_abbrs = ast.literal_eval(config[7])
skip_abbrs = ast.literal_eval(config[8])
move_abbrs = ast.literal_eval(config[9])
remove_abbrs = ast.literal_eval(config[10])
command_prefix_abbrs = ast.literal_eval(config[11])
command_abbrev_abbrs = ast.literal_eval(config[12])
command_list = ['play', 'disconnect', 'pause', 'resume', 'stop', 'now_playing', 'queue', 'skip', 'move', 'remove', 'command_prefix', 'command_abbrev']


# Data to keep track of
song_queue = []
current_song = ""

# Load names of currently downloaded songs
downloaded_songs = set()
song_dir = "songs"
for song in os.listdir(song_dir):
    downloaded_songs.add(song[:-4]) # don't include ".mp3"

# Specify whether to stream the music directly or download it
download = False

### The following is used to STREAM youtube/soundcloud audio instead of downloading it
# Copied from discord.py -> examples -> basic_voice.py
# https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py#L34
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = YoutubeDL(ytdl_format_options)

class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
##################################################################################


class HelperMethods():
    stopped = False

    async def joinChannel(ctx):
        user_is_in_vc = ctx.author.voice
        if user_is_in_vc:
            channel = ctx.author.voice.channel

            bot_is_in_vc = bot.voice_clients
            if not bot_is_in_vc:
                await channel.connect()
                return
            
            bot_is_in_same_vc = bot.voice_clients[0].channel == channel
            if not bot_is_in_same_vc:
                await bot.voice_clients[0].disconnect()
                await channel.connect()
        else:
            await ctx.send('Join a voice channel first.')

    async def get_song_info(arg):
        arg = str(arg)
        is_url = arg.startswith(r"https://")
        if is_url:
            song_url = arg
        else:
            search_term = arg
            search_results = VideosSearch(search_term, limit=1).result()
            song_url = search_results['result'][0]['link']

        song_id, song_title = HelperMethods.downloadMusic(song_url)
        return song_id, song_title, song_url

    async def play_next_song(ctx):
        if song_queue and not HelperMethods.stopped:
            next_song_id, next_song_title, next_song_url = song_queue.pop(0)
            await HelperMethods.playMusic(ctx, next_song_id, next_song_title, next_song_url)

    async def playMusic(ctx, song_id, song_title, song_url):
        vc = ctx.guild.voice_client    
        if not vc.is_playing():
            if download:
                audio = FFmpegPCMAudio(rf'songs/{song_id}.mp3')
                vc.play(audio, after=lambda e: asyncio.run_coroutine_threadsafe(HelperMethods.play_next_song(ctx), bot.loop))
            else:
                # streams the audio without downloading it!
                async with ctx.typing():
                    player = await YTDLSource.from_url(song_url, loop=bot.loop, stream=True)
                    ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

            vc.source = PCMVolumeTransformer(vc.source, volume=0.25)
            global current_song
            current_song = song_title
            await Basic_Commands.now_playing(bot, ctx)

    def downloadMusic(url):
        def download_filter(info, *, incomplete):
            duration = info.get('duration')
            if duration and duration > (600): # 10 minutes cap
                return 'The video/song is too long'

        ytdl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'match_filter': download_filter
        }

        song_id = song_title = ""
        if 'soundcloud' not in url:
            song_results = Video.getInfo(url, mode = ResultMode.json)
            song_id = song_results['id']
            song_title = song_results['title']
        else:
            res = urllib.request.urlopen(url).read().decode("utf8")
            song_id = re.findall(r'(?<=:)(\d*)(?=")', res)[0]
            song_title = re.findall(r'(?<=:title" content=")(.*?)(?=")', res)[0]
        
        if download and song_id not in downloaded_songs:
            downloaded_songs.add(song_id)

            with YoutubeDL(ytdl_opts) as ytdl:
                error_code = ytdl.download([url])
                print(error_code)

            if not os.path.exists("songs"):
                os.makedirs("songs")

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    song_id = re.findall(r"(?<=\[).+?(?=\])", file)[-1]
                    song_title = file[:-(len(f" [{song_id}].mp3"))]
                    os.replace(file, rf"songs/{song_id}.mp3")

        return song_id, song_title


class Basic_Commands(commands.Cog, name='Basic', description='Basic commands like play, now playing, disconnect, etc...'):

    @commands.command(help='Plays the song from the given search term or link\n- Searches for songs on YT and supports both YT or SC links\n- Searchs on YT by default, type \'sc\' before the search term to use SC\n- Supports YT and SC playlists', usage='<search term or link>', aliases=play_abbrs)
    async def play(self, ctx, *, arg):
        await HelperMethods.joinChannel(ctx)
        if not bot.voice_clients:
            return

        # search on soundcloud
        if arg[0:3] == 'sc ':
            search_term = arg[3:]
            search_term = urllib.parse.quote(search_term)
            url = r'https://soundcloud.com/search?q=' + search_term
            res = urllib.request.urlopen(url).read().decode('utf-8')
            sc_song_index = 0
            sc_song_url = re.findall(r'(?<=<li><h2>)(.*)(?=">)', res)[sc_song_index][10:]
            while r'/' not in sc_song_url: # link might be a profile instead of a song
                sc_song_index += 1
                sc_song_url = re.findall(r'(?<=<li><h2>)(.*)(?=">)', res)[sc_song_index][10:]
            sc_song_url = r'https://soundcloud.com/' + sc_song_url
            arg = sc_song_url

        song_id, song_title, song_url = await HelperMethods.get_song_info(arg)

        if song_id:
            if not ctx.voice_client.is_playing():
                await HelperMethods.playMusic(ctx, song_id, song_title, song_url)
                HelperMethods.stopped = False
            else:
                song_queue.append((song_id, song_title, song_url))
                await ctx.send(f"**added to queue:** {song_title}")
        else:
            await ctx.send("Song is too large to download")

    @commands.command(help='Displays the song that is currently playing', usage='', aliases=now_playing_abbrs)
    async def now_playing(self, ctx):
        await ctx.send(f"**__Now Playing:__** {current_song}")

    @commands.command(help='Disconnects the bot from the voice channel', usage='', aliases=disconnect_abbrs)
    async def disconnect(self, ctx):
        await self.stop(ctx)
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()

    @commands.command(help='Pauses the music', usage='', aliases=pause_abbrs)
    async def pause(self, ctx):
        vc = ctx.guild.voice_client
        if vc.is_playing():
            vc.pause()

    @commands.command(help='Resumes the music', usage='', aliases=resume_abbrs)
    async def resume(self, ctx):
        vc = ctx.guild.voice_client
        if vc.is_paused():
            vc.resume()

    @commands.command(help='Stops the music', usage='', aliases=stop_abbrs)
    async def stop(self, ctx):
        if not bot.voice_clients:
            return

        HelperMethods.stopped = True
        vc = ctx.guild.voice_client
        vc.stop()

    @commands.command(help='Changes the command prefix to the given char', usage='<char>', aliases=command_prefix_abbrs)
    async def command_prefix(self, ctx, arg):
        if len(arg) == 1:
            bot.command_prefix = arg
            await ctx.send(f'Updated command prefix to \'{arg}\'')

            with open('.config', 'r') as file:
                config = file.readlines()
            config[0] = arg + '\n'
            with open('.config', 'w') as file:
                file.writelines(config)
        else:
            await ctx.send('Please use a single character.')

    @commands.command(help='Adds the given abbreviation for the given command', usage='<add|remove|reset> <command> <abbreviation>', aliases=command_abbrev_abbrs)
    async def command_abbrev(self, ctx, *, arg):
        arg = arg.split(' ')
        if len(arg) >= 1:
            type = arg[0]
        if len(arg) >= 2:
            command = arg[1]
        if len(arg) >= 3:
            abbrev = arg[2]

        if type == 'add' or type == 'a':
            updated_command = bot.get_command(command)
            aliases = updated_command.aliases 
            aliases.append(abbrev)
            updated_command.aliases = aliases
            bot.remove_command(command)
            bot.add_command(updated_command)
            await ctx.send(f'Added command abbreviation \'{abbrev}\' for {command} command.')
        elif type == 'remove' or type == 'r' or type == 'rm':
            updated_command = bot.get_command(command)
            aliases = updated_command.aliases 
            aliases.remove(abbrev)
            updated_command.aliases = aliases
            bot.remove_command(command)
            bot.add_command(updated_command)
            await ctx.send(f'Removed command abbreviation \'{abbrev}\' for {command} command.')
        elif type == 'reset' or type == 'rst':
            if command == 'all':
                for command in command_list:
                    updated_command = bot.get_command(command)
                    with open('.config_default', 'r') as file:
                        config = file.readlines()
                    line = command_list.index(command) + 1
                    aliases = ast.literal_eval(config[line])
                    updated_command.aliases = aliases
                    bot.remove_command(command)
                    bot.add_command(updated_command)
                    await ctx.send(f'Reset command abbreviations for {command} command.')

                    with open('.config', 'r') as file:
                        config = file.readlines()
                    line = command_list.index(command) + 1
                    config[line] = str(aliases) + '\n'
                    with open('.config', 'w') as file:
                        file.writelines(config)
                return
            else:
                updated_command = bot.get_command(command)
                with open('.config_default', 'r') as file:
                    config = file.readlines()
                line = command_list.index(command) + 1
                aliases = ast.literal_eval(config[line])
                updated_command.aliases = aliases
                bot.remove_command(command)
                bot.add_command(updated_command)
                await ctx.send(f'Reset command abbreviations for {command} command.')

        with open('.config', 'r') as file:
            config = file.readlines()
        line = command_list.index(command) + 1
        config[line] = str(aliases) + '\n'
        with open('.config', 'w') as file:
            file.writelines(config)
bot.add_cog(Basic_Commands())


class Queue_Commands(commands.Cog, name='Queue', description='Queue related commands like queue, skip, move, etc...'):
    @commands.command(help='Displays the songs currently in queue the music', usage='', aliases=queue_abbrs)
    async def queue(self, ctx):
        if song_queue:
            queue_msg = "**Song Queue:**\n"
            for place, (_, song_title, _) in enumerate(song_queue):
                queue_msg += f'**[{place + 1}]** {song_title}\n'
            await ctx.send(queue_msg)
        else:
            await ctx.send("Song queue is empty.")

    @commands.command(help='Skips the current song and starts playing the next one in queue\n- If a search term or link is provided, then that is the next song that is played', usage='<optional search term or link>', aliases=skip_abbrs)
    async def skip(self, ctx, *args):
        if len(args):
            await Basic_Commands.stop(self, ctx)
            await Basic_Commands.play(self, ctx=ctx, arg=' '.join(list(args)))
        else:
            await Basic_Commands.stop(self, ctx)
            if song_queue:
                song_id, song_title, song_url = song_queue.pop(0)
                await HelperMethods.playMusic(ctx, song_id, song_title, song_url)

    @commands.command(help='Moves the song at the specified position (first argument) to the specified position (second argument) in the queue', usage='<queue pos1> <queue pos2>', aliases=move_abbrs)
    async def move(self, ctx, q_pos_src, q_pos_dst):
        q_pos_src = int(q_pos_src) - 1
        q_pos_dst = int(q_pos_dst) - 1
        if q_pos_src < len(song_queue) and q_pos_dst < len(song_queue) and q_pos_src >= 0 and q_pos_dst >= 0 and q_pos_src != q_pos_dst: # sanitize input
            song_id, song_title, song_url = song_queue.pop(q_pos_src)
            song_queue.insert(q_pos_dst, (song_id, song_title, song_url))
            await ctx.send(f"**moved song to position {q_pos_dst + 1}:** {song_title}")

    @commands.command(help='Removes the song at the specified position in the queue', usage='<queue pos>', aliases=remove_abbrs)
    async def remove(self, ctx, q_pos):
        q_pos = int(q_pos) - 1
        if q_pos < len(song_queue) and q_pos >= 0: # sanitize the input
            _, song_title, _ = song_queue.pop(q_pos)
            await ctx.send(f"**removed song at position {q_pos + 1}:** {song_title}")
bot.add_cog(Queue_Commands())


def main():
    token = str(sys.argv[1])
    bot.run(token)
    
if __name__ == '__main__':
    main()