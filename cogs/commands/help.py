import math
import discord

from discord.ext import commands
from utils import functions

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        
    @commands.command(aliases=['h','?'])
    async def help(self, ctx, page=1):
        'Displays the help command'
        em = discord.Embed()
        em.title = 'Help Command'
        command_list = ''        
        cog_list = [c for c in self.bot.cogs.keys()]   
        page_count = math.ceil(len(cog_list) / 4)
        
        page = int(page)
        if page > page_count or page<1:
            await ctx.send(f'Page number \'{page}\' not found.')
            return
        
        cogs_needed = []
        for i in range(4):
            x = i + (int(page) - 1) * 4
            try:
                cogs_needed.append(cog_list[x])
            except IndexError:
                pass
        
        for cog in cogs_needed:
            command_list = ''
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                if command.parent:
                    continue                
                command_list += f'**{ctx.prefix}{command.name}** - {command.help}\n'
            command_list += '\n'            
            em.add_field(name=cog, value=command_list, inline=False)        
        em.set_footer(text=f'Requested by {ctx.message.author}', icon_url=functions.get_avatar(ctx.message.author))
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Help(bot))