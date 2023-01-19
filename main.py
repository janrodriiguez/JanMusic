import discord
import random
import time
import os
import youtube_dl
import asyncio
from discord import app_commands
from  discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

#For a more secure, we loaded the .env file and assign the token value to a variable .
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

#Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents=discord.Intents.all()

#Command prefix is setup here, this is what you have to type to issue a command to the bot.
prefix = '!'
client = commands.Bot(command_prefix=prefix, intents=intents)

#Removed the help command to create a custom help guide
client.remove_command('help')

#--------------------------------------------------------Music Bot--------------------------------------------------------------#

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

#--------------------------------------------------------Events--------------------------------------------------------------#

#here we define the discord bot status and a print message on the terminal when it's on.
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!help"))
    print(f"Conectado como: {client.user}")


#--------------------------------------------------------Music Bot Events--------------------------------------------------------------#

@client.event
async def on_message(msg):
    if msg.content.startswith("!play"):

        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        try:
            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            song_name = data.get('title', None)
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[msg.guild.id].play(player)
            embed = discord.Embed(
                title='Now playing',
                description=f'{song_name}',
                color=discord.Colour.from_rgb(32, 34, 37)
            )
            await msg.channel.send(embed=embed)
        except Exception as err:
            print(err)
            
    if msg.content.startswith("!pause"):
        embed = discord.Embed(
            #title='Canción pausada',
            description='Paused the song.',
            color=discord.Colour.from_rgb(32, 34, 37)
        )
        await msg.channel.send(embed=embed)

        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    if msg.content.startswith("!resume"):
        embed = discord.Embed(
            #title='Canción renaudada',
            description='Resumed the song.',
            color=discord.Colour.from_rgb(32, 34, 37)
        )
        await msg.channel.send(embed=embed)
        
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    if msg.content == ("!stop"):
        await msg.add_reaction("👌")


        try:
            voice_clients[msg.guild.id].stop()
        except Exception as err:
            print(err)

    if msg.content == ("!disconnect"):
        await msg.add_reaction("👌")
        try:
            await voice_clients[msg.guild.id].disconnect()
            voice_clients[msg.guild.id] = None
        except Exception as err:
            print(err)

    #This help embed will show the commands available on the bot just by using "!help"
    if msg.content == ("!help"):
        embed = discord.Embed(
            #title=
            #description=
            colour=discord.Colour.from_rgb(32, 34, 37)
        )

        embed.set_author(name='Help Commands', icon_url='https://media.istockphoto.com/id/1012390100/pt/vetorial/vector-logo-letter-j-wing.jpg?s=170667a&w=0&k=20&c=vLF_KnEp86Py-0x9W3SmsHPeeLAiqGQrBKQq1K7VmDU=')
        embed.add_field(name="Everyone commands", value="`help`, `play`, `pause`, `ping`, `resume`, `stop`, `disconnect`", inline=False)
        embed.set_footer(text="Type '.help <CommandName>' for details on a command")
        #embed.add_field(name="", value="", inline=False)

        await msg.channel.send(embed=embed)

#Embed that specifies the bot ping
    if msg.content == ("!ping"):
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(32, 34, 37)
        )

        ping = round(client.latency * 1000)
        embed.add_field(name="", value="🟢 `" + str(ping) + "ms`", inline=False)

        await msg.channel.send(embed=embed)

#token
client.run(TOKEN)