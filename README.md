# Discord Music Bot

A simple discord music bot that can play songs from YouTube or SoundCloud through the voice channel.

## Features

Currently the bot can only play music through YT links.

Here is a list of what still needs to be implemented and improved:

* Play music through SC links.
* Let the user search for music (YT and SC).
* Queue up songs to play.
* Download music faster or find a way to stream it (this has been difficult to figure out).

## Commands

**/play** &lt;link&gt;

* Plays the song from the given link.
* This link should either be a YT or SC link. For example: https://youtu.be/dQw4w9WgXcQ.

**/disconnect**
* Disconnects the bot from the voice channel.

**/pause**
* Pauses the music.

**/resume**
* Resumes the music.

**/stop**
* Stops the music.

### Not yet implemented

**/skip**
* Skips the current song and starts playing the next one in queue.

**/queue**
* Displays the songs currently in queue.

**/command_prefix** &lt;char&gt;
* Changes the command prefix to be the given character instead.

**/help**
* Displays a list of commands.


## Getting Started

### Dependencies

* Python 3.10.2
* discord.py[voice]
* yt_dlp

All of the dependendent libraries are already included in the python environment, 'bot-env'. That way nothing additional is required to be downloaded or installed. 

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Author

Coded from scratch by [Kidus Yohannes](https://kidusyohannes.me/)

## Version History

* 0.1
    * Initial Release
    * Basic functionality implemented

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

Useful resources I used:
* Documentation for [discord.py](https://discordpy.readthedocs.io/en/stable/index.html)
* Documentation for [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* And obviously [Stack Overflow](https://stackoverflow.com/)
