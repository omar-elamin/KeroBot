import discord
import datetime
import random
import aiofiles

from discord.ext import commands
from utils import checks
from utils import functions


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.reaction_roles = []

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Client] {self.bot.user.name} is online.')
        game = discord.Game('with your feelings')
        await self.bot.change_presence(status=discord.Status.online, activity=game)
    
        guildCount = len(self.bot.guilds)
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Guilds] Bot currently in {guildCount} guilds.')
        for guild in self.bot.guilds:
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Guilds] Connected to guild: {guild.name}, Owner: {guild.owner}')
            
        blacklist_data = functions.read_json('blacklist')
        checks.blacklisted_users = blacklist_data['blacklist']
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] Current blacklist:')
        for user_id in checks.blacklisted_users:
            user = self.bot.get_user(user_id)
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] - {user.name}')
        global starttime
        starttime = datetime.datetime.utcnow()
        
        for file in ['reactionroles.txt']:
            async with aiofiles.open(file, mode='a') as temp:
                pass
        async with aiofiles.open('reactionroles.txt', mode='r') as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(' ')
                self.bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip('\n')))
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member == self.bot.user:
            pass
        else:
            for role_id, msg_id, emoji in self.bot.reaction_roles:
                if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode('utf-8')):
                    await payload.member.add_roles(self.bot.get_guild(payload.guild_id).get_role(role_id), reason='reaction')
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.member == self.bot.user:
            pass
        else:
            for role_id, msg_id, emoji in self.bot.reaction_roles:
                if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode('utf-8')):
                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(self.bot.get_guild(payload.guild_id).get_role(role_id), reason='reaction')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} ran: {ctx.message.content} in guild: {ctx.guild.name}')
        loggingchannel = self.bot.get_channel(751158338821029919)
        randomcolour = "%06x" % random.randint(0, 0xFFFFFF)
        log = discord.Embed(title='Logging', description=f'{ctx.author} ran: {ctx.message.content} in guild: {ctx.guild.name}', colour=discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        await loggingchannel.send(embed=log)
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send('''```py
{}```'''.format(error))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}')
        loggingchannel = self.bot.get_channel(751158338821029919)
        randomcolour = "%06x" % random.randint(0, 0xFFFFFF)
        log = discord.Embed(title='Error Logging', description=f'{ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}', colour=discord.Colour.from_rgb(255,0,0))
        await loggingchannel.send(embed=log)
        
def setup(bot):
    bot.add_cog(Events(bot))