# JanMusic
Since a lot of discord music bots are being blocked by youtube nowadays, I've decided to write up a quick project that will aloww anyone to host their own discord bot. This bot includes the following commands:

!help - displays all the available commands
!play <youtube_url> - the bot joins your voice channel and starts streaming the song you selected\
!pause - pauses the current song being played\
!resume - resumes playing the current song\
!stop - stops the song and removes it from the queue\
!disconnect - the bot disconnects from your voice channel

# Installation
To run the discord bot all you need is python 3.4 or above.\
Then run `pip install -r requirements.txt` to install all of the python dependencies.\
Please note that you will also need to have [ffmpeg](https://ffmpeg.org/download.html) installed and make sure that the path to the bin folder is in your computer environment variables.

# Token
Remember that you need to have your token setup in your environment variables as well and it should be in the .env file after TOKEN=xxxxxxxxxxxxxxxxx.
