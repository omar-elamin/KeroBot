import discord
from discord.ext import commands
import datetime

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        bot = ctx.bot
        vc = ctx.author.voice.channel
        voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voiceClient and voiceClient.is_connected():
            await voiceClient.move_to(vc)
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has moved to {vc} in {ctx.guild.name}\n")
            await ctx.send(f'Joined `{vc.name}`')
        else:
            await vc.connect()
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has connected to {vc} in {ctx.guild.name}\n")
            await ctx.send(f'Joined `{vc.name}`')
    
    @commands.command()
    async def leave(self, ctx):
        bot = ctx.bot
        vc = ctx.author.voice.channel
        voiceClient = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voiceClient and voiceClient.is_connected():
            await voiceClient.disconnect()
            await ctx.send(f'Left `{vc.name}`')
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] The bot has disconnected from {vc.name} in {ctx.guild.name}\n")
        else:
            await ctx.send(f"`{ctx.author.name}` you fat retard i'm not connected to a vc")
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Music] {ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}')
    
def setup(bot):
    bot.add_cog(Music(bot))
