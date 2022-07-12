
import sys
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer, Color
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch, Video, ResultMode
from pretty_help import PrettyHelp, DefaultMenu
import os
import re
import asyncio
import urllib

command_prefix = '/' # all commands should start with '/'
ending_note = "Check the github for a list of all the commands and their descriptions:\nhttps://github.com/MrYo531/music-bot"
help_command = PrettyHelp(color=Color.blue(), ending_note=ending_note, index_title='Commands')
menu = DefaultMenu(delete_after_timeout=True)
bot = commands.Bot(command_prefix=command_prefix, help_command=help_command, menu=menu)

# all possible commands and their abbreviations
play_abbrs = ['p']
disconnect_abbrs = ['dc']
pause_abbrs = ['ps']
resume_abbrs = ['rs']
stop_abbrs = ['st']
now_playing_abbrs = ['np']
queue_abbrs = ['q']
skip_abbrs = ['sk']
move_abbrs = ['mv', 'm']
remove_abbrs = ['rm']

# keep track of the songs to play next
song_queue = []
current_song = ""
#stopped = False

# load and keep track of downloaded song list
downloaded_songs = set()
song_dir = "songs"
for song in os.listdir(song_dir):
    downloaded_songs.add(song[:-4]) # don't include ".mp3"
#print(downloaded_songs)

class HelperMethods():
    def __init__(self):
        self.stopped = False

    async def joinChannel(self, ctx):
        if ctx.author.voice: # user is in voice channel
            channel = ctx.author.voice.channel
            if not bot.voice_clients: # bot is not already in voice channel
                await channel.connect()
            elif bot.voice_clients[0].channel != channel: # bot is not already in same voice channel
                await bot.voice_clients[0].disconnect()
                await channel.connect()
        else:
            await ctx.send('Join a voice channel first.')

    async def get_song_info(self, arg):
        arg = str(arg)
        if arg.startswith(r"https://"): # url link
            song_url = arg
        else: # search term
            search_results = VideosSearch(str(arg), limit=1).result()
            song_url = search_results['result'][0]['link']

        song_id, song_title = self.downloadMusic(song_url)
        return song_id, song_title

    async def play_next_song(self, ctx):
        if song_queue and not self.stopped:
            next_song_id, next_song_title = song_queue.pop(0)
            await self.playMusic(ctx, next_song_id, next_song_title)

    async def playMusic(self, ctx, video_id, video_title):
        vc = ctx.guild.voice_client    
        if not vc.is_playing():
            audio = FFmpegPCMAudio(rf'songs/{video_id}.mp3')
            # play the current song then play the next one in queue after it finishes
            vc.play(audio, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next_song(ctx), bot.loop))
            vc.source = PCMVolumeTransformer(vc.source, volume=0.25)
            global current_song
            current_song = video_title
            await Basic_Commands.now_playing(self, ctx)

    def downloadMusic(self, url):
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
        if not 'soundcloud' in url:
            song_results = Video.getInfo(url, mode = ResultMode.json)
            song_id = song_results['id']
            song_title = song_results['title']
            #print("video info: ", song_id, song_title)
        else:
            res = urllib.request.urlopen(url).read().decode("utf8")
            song_id = re.findall(r'(?<=:)(\d*)(?=")', res)[0]
            song_title = re.findall(r'(?<=:title" content=")(.*?)(?=")', res)[0]
            #print(song_id, song_title)
        
        if not song_id in downloaded_songs: # download song if not already downloaded
            downloaded_songs.add(song_id)

            with YoutubeDL(ytdl_opts) as ytdl: # works with SC links too apparently 
                error_code = ytdl.download([url])

            if not os.path.exists("songs"):
                os.makedirs("songs")

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    song_id = re.findall(r"(?<=\[).+?(?=\])", file)[-1]
                    song_title = file[:-(len(f" [{song_id}].mp3"))]
                    os.replace(file, rf"songs/{song_id}.mp3")

        return song_id, song_title

class Basic_Commands(commands.Cog, name='Basic', description='Basic commands like play, now playing, disconnect, etc...'):
    def __init__(self):
        self.hm = HelperMethods()

    @commands.command(help='Plays the song from the given search term or link\n- Searches for songs on YT and supports both YT or SC links', usage='<search term or link>', aliases=play_abbrs)
    async def play(self, ctx, *, arg):
        await self.hm.joinChannel(ctx)
        if not bot.voice_clients: # bot is not connected to voice channel
            return

        song_id, song_title = await self.hm.get_song_info(arg)

        if song_id:
            #print(song_id, "\n", song_title)
            if not ctx.voice_client.is_playing(): # bot is not playing music yet
                await self.hm.playMusic(ctx, song_id, song_title)
                #global stopped
                self.hm.stopped = False
            else: # bot is already playing music, so just queue the song
                song_queue.append((song_id, song_title))
                await ctx.send(f"**added to queue:** {song_title}")
        else:
            await ctx.send("Song is too large to download.")

    @commands.command(help='Displays the song that is currently playing', usage='', aliases=now_playing_abbrs)
    async def now_playing(self, ctx):
        await ctx.send(f"**__Now Playing:__** {current_song}")

    @commands.command(help='Disconnects the bot from the voice channel', usage='', aliases=disconnect_abbrs)
    async def disconnect(self, ctx):
        await Basic_Commands.stop(ctx)
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
        if not bot.voice_clients: # bot is not connected to voice channel
            return

        self.hm.stopped = True
        vc = ctx.guild.voice_client
        vc.stop()
bot.add_cog(Basic_Commands())

class Queue_Commands(commands.Cog, name='Queue', description='Queue related commands like queue, skip, move, etc...'):
    def __init__(self):
        self.hm = HelperMethods()

    @commands.command(help='Displays the songs currently in queue the music', usage='', aliases=queue_abbrs)
    async def queue(self, ctx):
        if song_queue:
            queue_msg = "**Song Queue:**\n"
            for place, (_, song_title) in enumerate(song_queue):
                queue_msg += f'**[{place}]** {song_title}\n'
            await ctx.send(queue_msg)
        else:
            await ctx.send("Song queue is empty.")

    @commands.command(help='Skips the current song and starts playing the next one in queue\n- If a search term or link is provided, then that is the next song that is played', usage='<optional search term or link>', aliases=skip_abbrs)
    async def skip(self, ctx, *args):
        if len(args):
            await Basic_Commands.stop(self, ctx)
            await Basic_Commands.play(self, ctx=ctx, arg=''.join(list(args)))
        else:
            await Basic_Commands.stop(self, ctx)
            if song_queue:
                song_id, song_title = song_queue.pop(0)
                await self.hm.playMusic(ctx, song_id, song_title)

    @commands.command(help='Moves the song at the specified position (first argument) to the specified position (second argument) in the queue', usage='<queue pos1> <queue pos2>', aliases=move_abbrs)
    async def move(self, ctx, q_pos_src, q_pos_dst):
        q_pos_src = int(q_pos_src)
        q_pos_dst = int(q_pos_dst)
        if q_pos_src < len(song_queue) and q_pos_dst < len(song_queue) and q_pos_src >= 0 and q_pos_dst >= 0 and q_pos_src != q_pos_dst: # sanitize input
            song_id, song_title = song_queue.pop(q_pos_src)
            song_queue.insert(q_pos_dst, (song_id, song_title))
            await ctx.send(f"**moved song to position {q_pos_dst}:** {song_title}")

    @commands.command(help='Removes the song at the specified position in the queue', usage='<queue pos>', aliases=remove_abbrs)
    async def remove(self, ctx, q_pos):
        q_pos = int(q_pos)
        if q_pos < len(song_queue) and q_pos >= 0: # sanitize input
            _, song_title = song_queue.pop(q_pos)
            await ctx.send(f"**removed song at position {q_pos}:** {song_title}")
bot.add_cog(Queue_Commands())

def main():
    token = str(sys.argv[1]) # the first argument passed to the script should be the bot token
    bot.run(token)
    
if __name__ == '__main__':
    main()
