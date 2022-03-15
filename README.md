# Discord Music Bot

A simple Discord bot that plays songs from YouTube or SoundCloud through the voice channel.

## Features

Commands can be abbreviated. For example: /p is the same as /play.

Currently, the bot can only play music through YT links.

Here is a list of what still needs to be implemented and improved:

* Play music through SC links
* Let the user search for music instead of passing a link
* Queue up songs to play
* Register new command abbreviations
* Download music faster or find a way to stream it directly (this has been difficult to figure out)

## Commands

**/play** &lt;link&gt;

* Plays the song from the given link
* This link should either be a YT or SC link
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
    * **/r**
    * **/rs**

**/stop**
* Stops the music
* Can also be called with: 
    * **/s**

### Not yet implemented

**/skip**
* Skips the current song and starts playing the next one in queue

**/queue**
* Displays the songs currently in queue

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

You can install Python from the Microsoft Store and FFmpeg using [this](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) guide.

The python libaries (discord.py and yt_dlp) are already installed in the python virtual environment, 'bot-env'. That way, you can follow these instructions without having to install them yourself.

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

* 0.1
    * Initial Release
    * Basic functionality implemented

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

* Documentation for [discord.py](https://discordpy.readthedocs.io/en/stable/index.html)
* Documentation for [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* And obviously [Stack Overflow](https://stackoverflow.com/)
