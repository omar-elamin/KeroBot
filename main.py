import discord
import datetime
import os
import time

from discord.ext import commands
from dotenv import load_dotenv
from utils import checks
from utils import functions

load_dotenv()
botToken = os.getenv('botToken')

intents = discord.Intents.all()
allowed_mentions = discord.AllowedMentions(everyone=False)
bot = commands.Bot(command_prefix=os.getenv('prefix'), description='Kero Help Command', intents=intents, allowed_mentions = allowed_mentions)

extensions = [
    'cogs.commands.help',
    'cogs.commands.moderation',
    'cogs.commands.developer',
    'cogs.commands.misc',
    'cogs.music.music',
    'cogs.events',
    'cogs.tf'
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Extensions] {extension} loaded successfully")
        except Exception as e:
            print("[{} INFO]: [Extensions] {} didn't load {}".format(datetime.datetime.utcnow().replace(microsecond=0), extension, e))
@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    else:
        channel = message.channel
        if '<@723524131970351194>' in message.content or '<@!723524131970351194>' in message.content:
            keroInfo = discord.Embed(title='Kero Bot', description='`Prefix: ,` (run ,help for help)', color=0xbc0a1d)
            keroInfo.add_field(name='Owner', value='`elmon#0001`')
            keroInfo.add_field(name='Developers', value='`elmon#0001`, `speed#3413`')
            await channel.send(embed=keroInfo)
             #  Guild specific features
        if isinstance(message.channel, discord.channel.DMChannel):
            pass
        else:
            if channel.guild.name == 'The Circus':
                for x in ['fran', 'complex']:
                    if x in message.content.lower():
                        await channel.send('Fran is a homosexual.')
                if 'xd' in message.content.lower():
                    await message.delete()
            if channel.guild.name == 'Radical Roller Rink':
                if '!rank' in message.content and channel.name != 'bot-spam':
                    await channel.send(f'{message.author.mention} <#741113645487882381>')
                    time.sleep(1.5)
                    await channel.purge(limit=1)
    blacklisted = discord.Embed(description='It appears you were blacklisted by a developer.')
    blacklisted.title = 'Hmm'
    blacklisted.color = 0xFF0000
    blacklisted.set_footer(text="DM any dev (,listdevs) to be unblacklisted.")
    if message.author.id in checks.blacklisted_users and message.content.startswith(bot.command_prefix):

        await message.channel.send(embed=blacklisted)
        print("[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] {} tried running command {}".format(message.author, message.content))
        return
    if isinstance(message.channel, discord.channel.DMChannel):
        dmEmbed = discord.Embed()
        dmEmbed.description = message.content
        dmEmbed.color = 0xbc0a1d
        dmEmbed.set_author(icon_url=message.author.avatar_url, name=message.author.name)
        await bot.get_channel(751885078463774810).send(embed=dmEmbed)
        return
    await bot.process_commands(message)
bot.run(botToken)
