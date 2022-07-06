# Discord Music Bot

A simple Discord bot that plays songs from YouTube or SoundCloud through the voice channel.

## Features

Commands can be abbreviated. For example: /p is the same as /play.

A song that has already been downloaded will be played right away instead of waiting to downloading it again.

Here is a list of what still needs to be implemented and improved:

* Search for music using SC
* fast forward / rewind command, help command
* Register new command abbreviations
* Test that it works on multiple servers simultaneously 
* Download music faster or find a way to stream it directly (this has been difficult to figure out)
* Support on Linux/Mac OS (reconfirm installation instructions are accurate)

## Commands

**/play** &lt;search term or link&gt;

* Plays the song from the given search term or link
* Searchs for songs on YT and supports both YT or SC links
* Can also be called with: 
    * **/p**

**/disconnect**
* Disconnects the bot from the voice channel
* Can also be called with: 
    * **/dc**
    * **/leave**
    * **/l**

**/pause**
* Pauses the music
* Can also be called with: 
    * **/pp**
    * **/ps**

**/resume**
* Resumes the music
* Can also be called with: 
    * **/rs**

**/stop**
* Stops the music
* Can also be called with: 
    * **/st**

**/now_playing**
* Displays the song that is currently playing
    * **/np**

**/queue**
* Displays the songs currently in queue
    * **/q**

**/skip** &lt;optional search term or link&gt;
* Skips the current song and starts playing the next one in queue
* If a search term or link is provided, then that is the next song that is played
    * **/sk**
    * **/pskip**
    * **/playskip**

**/move** &lt;queue position&gt; &lt;queue position&gt;
* Moves the song at the specified position (first argument) to the specified position (second argument) in the queue
    * **/mv**
    * **/m**

**/remove** &lt;queue position&gt;
* Removes the song at the specified position in the queue
    * **/rm**

### Not yet implemented    

**/command_prefix** &lt;char&gt;
* Changes the command prefix to be the given character instead

**/help**
* Displays a list of commands

## Running the Bot

These instructions assume you're using Windows and that you've already created a bot account.

If you haven't, follow [these](https://discordpy.readthedocs.io/en/stable/discord.html#) instructions for creating a bot and inviting it to your server.

The only required bot permissions are:
* Read Messages/View Channels [General]
* Send Messages [Text]
* Embed Links [Text]
* Connect [Voice]
* Speak [Voice]

### Dependencies

* Python 3.10.2
* FFmpeg
* discord.py[voice]
* yt_dlp
* soundcloud-dl
* youtube-search-python

You can install Python from the Microsoft Store and FFmpeg using [this](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) guide.

The python libaries are already installed in the python virtual environment, 'bot-env'. That way, you can follow these instructions without having to manually install them yourself.

### Steps

* Download this repo as a .zip and extract it to a location on your computer

* Open up Command Prompt and navigate to where you extracted the folder
```
cd C:\Users\Kidus\Downloads\music-bot-main\
```

* Run the script using the python executable from the virtual environment and passing your bot token as the first argument
```
bot-env\Scripts\python.exe run.py <token>
```

And that's it. In Discord, join a voice channel and type the following command in a text channel to play a song:
```
/play https://youtu.be/dQw4w9WgXcQ
```

## Author

Coded from scratch by [Kidus Yohannes](https://kidusyohannes.me/)

## Version History

* 0.1 - 03/14/2022
    * Initial Release
    * Basic functionality implemented (play, pause, resume, stop, dc)
* 0.2 - 06/27/2022
    * Added SoundCloud link support
    * Added YT search capabilities
    * Added queue support and related commands (now playing, skip, move, etc...)
* 0.3 - 07/06/2022
    * Added functionality to check for downloaded songs
    * Added remove command

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

* Documentation for [discord.py](https://discordpy.readthedocs.io/en/stable/index.html)
* Documentation for [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* And obviously [Stack Overflow](https://stackoverflow.com/)
