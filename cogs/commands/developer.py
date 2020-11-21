import discord
import datetime
import asyncio

from discord.ext import commands
from utils import checks
from utils import functions

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)    
    
    @commands.command(help='Shuts down the bot', aliases=['kill', 'restart'])
    @checks.is_dev()
    async def shutdown(self, ctx):
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} has shut down the bot.', colour=0xbc0a1d))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Shutdown] {ctx.author.name}: shutting down {self.bot.user.name} command sent in {ctx.guild.name}')
        for player in self.bot.music.player_manager.find_all():
            self.bot.music.player_manager.remove(player.guild_id)
            await self.connect_to(player.guild_id, None)
        await self.bot.logout()
    
    @commands.command(name='eval')
    @checks.is_dev()
    async def evaluate(self, ctx, *, cmd):
        'Executes a line of code.'
        try:
            result = eval(cmd)
            if asyncio.iscoroutine(result):
                result = await result
            await ctx.send(f'''```py
{result}```''')
        except Exception as e:
            await ctx.send(f'''```py
{type(e).__name__}: {e}```''')
    
    @commands.command(pass_context=True)
    @checks.is_dev()
    async def showguilds(self, ctx):
        message = ""
        for x in self.bot.guilds:
            message += f'{x.name} | {len(x.members)} members\n'
        embedGuilds = discord.Embed(description=message, title=f'Guilds [{len(self.bot.guilds)}]', colour=0xbc0a1d)
        await ctx.send(embed=embedGuilds)
        
    @commands.command(pass_context=True)
    @checks.is_dev()
    async def blacklist(self, ctx, *, user: discord.User):
        checks.blacklisted_users.append(user.id)
        data = functions.read_json('blacklist')
        data['blacklist'].append(user.id)
        functions.write_json('blacklist',data)
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been blacklisted.', colour=0xbc0a1d))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Added {user.name} to the blacklist.')
    
    
    @commands.command(pass_context=True)
    @checks.is_dev()
    async def unblacklist(self, ctx, *, user: discord.User): 
        try:
            checks.blacklisted_users.remove(user.id)
            data = functions.read_json('blacklist')
            data['blacklist'].remove(user.id)
            functions.write_json('blacklist',data)
            await ctx.send(embed=discord.Embed(description=f'{user.name} has been unblacklisted.', colour=0xbc0a1d))
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Removed {user.name} from the blacklist.')
        except ValueError:
            ctx.send(embed=discord.Embed(description=f'{user.name} is not currently blacklisted.', colour=0xbc0a1d))
    
    
    @commands.command(pass_context=True)
    @checks.is_dev()
    async def showblacklist(self, ctx):
        if not checks.blacklisted_users:
            await ctx.send(embed=discord.Embed(description='No users currently blacklisted.', colour=0xbc0a1d))
        else:
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the blacklist.')
            blacklistMessage = ''
            for user in checks.blacklisted_users:
                user = self.bot.get_user(user)
                blacklistMessage += f'- {user.name}\n'
            blacklistEmbed = discord.Embed(description=blacklistMessage, title='Current blacklist', colour = 0xbc0a1d)
            await ctx.send(embed=blacklistEmbed)
    
    @commands.command(pass_context=True)
    @checks.is_dev()
    async def listnodm(self, ctx):
        if not checks.nodm_ids:
            await ctx.send(embed=discord.Embed(description='No users currently opted out of DMs.', colour=0xbc0a1d))
        else:
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the No-DM List.')
            nodmMessage = ''
            for user in checks.nodm_ids:
                user = self.bot.get_user(user)
                nodmMessage += f'- {user.name}\n'
            nodmEmbed = discord.Embed(description=nodmMessage, title='Current No-DM list', colour = 0xbc0a1d)
            await ctx.send(embed=nodmEmbed)
    
def setup(bot):
    bot.add_cog(Developer(bot))
