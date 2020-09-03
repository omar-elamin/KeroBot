import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(ctx):
        vc = ctx.author.voice.channel
        voiceClient discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voiceClient.is_connected():
            await voiceClient.move_to(vc)
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has moved to {vc} in {ctx.guild.name}\n")
            await ctx.send(f'Joined `{vc.name}`')
        else:
            await channel.connect()
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has connected to {vc} in {ctx.guild.name}\n")
            await ctx.send(f'Joined `{vc.name}`')
