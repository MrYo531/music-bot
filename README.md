# Discord Music Bot

A simple Discord bot that plays songs from YouTube or SoundCloud through the voice channel.

## Features

* Can search for songs on YouTube or SoundCloud.

* Can stream songs directly or with the option to download them instead. 

* Commands can be abbreviated. For example: /p is the same as /play.

* A song that has already been downloaded will be played right away instead of waiting to downloading it again.

* Can update the command prefix (saved to config file).

* Can add, remove, or reset command abbreviations (saved to config file).

Here is a list of what still needs to be implemented and improved:

* Fast forward and rewind command [less prio]
* Test that it works on multiple servers simultaneously 
* Try hosting on AWS with a fast internet connection (will download music faster?)
* Support on Linux/Mac OS (confirm installation instructions are accurate and that the code runs fine on other platforms)
* Try running publicly, allowing anyone to invite the bot.

## Commands

**/play** &lt;search term or link&gt;

* Plays the song from the given search term or link
* Searchs for songs on YT or SC and supports both YT and SC links
* Searchs on YT by default, type 'sc' before the search term to use SC
* Supports YT and SC playlists
* Can also be called with: 
    * **/p**

**/disconnect**
* Disconnects the bot from the voice channel
* Can also be called with: 
    * **/dc**

**/pause**
* Pauses the music
* Can also be called with: 
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
* Can also be called with: 
    * **/np**

**/queue**
* Displays the songs currently in queue
* Can also be called with: 
    * **/q**

**/skip** &lt;optional search term or link&gt;
* Skips the current song and starts playing the next one in queue
* If a search term or link is provided, then that is the next song that is played
* Can also be called with: 
    * **/sk**

**/move** &lt;queue position&gt; &lt;queue position&gt;
* Moves the song at the given position (first argument) to the given position (second argument) in the queue
* Can also be called with: 
    * **/mv**

**/remove** &lt;queue position&gt;
* Removes the song at the given position in the queue
* Use 'all' to remove all the songs in the queue
* Can also be called with: 
    * **/rm**

**/clear**
* Removes all the songs in the queue
* Can also be called with: 
    * **/cl**

**/command_prefix** &lt;character&gt;
* Changes the command prefix to the given character
* Can also be called with: 
    * **/cp**

**/command_abbrev** &lt;add|remove|reset&gt; &lt;command&gt; &lt;abbreviation&gt;
* Adds (or removes) the given abbreviation for the given command (can be abbreviated)
* Can also reset the abbreviations for the given command (ignore the abbreviation argument)
* Can also reset the abbreviations for all commands (use 'all' for the command argument)
* Can also be called with: 
    * **/ca &lt;a|rm|rst&gt;**

**/download_songs** &lt;true|false|?&gt;
* Controls whether to download songs or to stream them (default).
* Can also be called with: 
    * **/ds &lt;t|f|' '&gt;**

**/help**
* Displays a list of commands
* Can use with a specific command (can be abbreviated) for more info

### Not yet implemented    

**/fast_forward** &lt;seconds&gt;
* Fast forwards the current song the given amount of seconds
    * **/ff**

**/rewind** &lt;seconds&gt;
* Rewinds the current song the given amount of seconds
    * **/rw**

## Running the Bot

These instructions assume you're using Windows and that you've already created a bot account. (planning to update these instructions to work for all platforms)

If you haven't already, follow [these](https://discordpy.readthedocs.io/en/stable/discord.html#) instructions for creating a bot and inviting it to your server.

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
* discord-pretty-help

Other common libraries:
* os
* re
* asyncio
* urllib
* json

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

Coded 'mostly' from scratch by [Kidus Yohannes](https://kidusyohannes.me/)

## Version History

Beta
* 0.1 - 03/14/2022
    * Initial Release
    * Basic functionality implemented (play, pause, resume, stop, disconnect)
* 0.2 - 06/27/2022
    * Added SoundCloud link support
    * Added YT search capabilities
    * Added queue support and related commands (now playing, skip, move, etc...)
* 0.3 - 07/06/2022
    * Added functionality to check for downloaded songs
    * Added remove command
* 0.4 - 07/11/2022
    * Added help method with command descriptions
    * Refactored code to use classes/cogs
* 0.5 - 07/15/2022
    * Added command_prefix command
    * Added command_abbrev command
* 0.6 - 07/26/2022
    * Added support for searching on SoundCloud
* 0.7 - 08/16/2022
    * Added support for streaming songs directly (instead of downloading them)
* 0.8 - 12/25/2022
    * Added download_songs command for controlling whether to download or stream songs
    * Fixed a lot bugs and added several warning/helper messages
* 0.9 - 1/8/2023
    * Added playlist support for both YT and SC
    * Added functionality to disconnect after being inactive for a period of time
    * Added clear command
    * Fixed more bugs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

* Documentation for [discord.py](https://discordpy.readthedocs.io/en/stable/index.html)
* Documentation for [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* Code for [streaming audio](https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py#L34)
* And obviously [Stack Overflow](https://stackoverflow.com/)
