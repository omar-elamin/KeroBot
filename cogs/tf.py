import discord
import datetime
import asyncio
import json
import requests

from discord.ext import commands
from utils import checks
from utils import functions

class TF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def hit_endpoint(self, command):
        url = [CENSORED_URL]
        payload = {}
        headers = {}
    
        response = json.loads(requests.request("GET", url, headers=headers, data = payload, timeout=5).text)
        return response['response']
    
    @commands.command()
    @checks.is_tf_and_perms()
    async def starttf(self, ctx):
        'Starts the TotalFreedom server'
        em = discord.Embed()
        try:
            attempt = self.hit_endpoint('start')
            print(attempt)
        except Exception as e:
            em.title='Command error'
            em.colour = 0xFF0000
            em.description='Something went wrong'
            print(f'Error while starting server: {e}')
            await ctx.send(embed=em)
        else:
            em.title = 'Success'
            em.colour = 0x00FF00
            em.description = f'Server started.'
            await ctx.send(embed=em)
    
def setup(bot):
    bot.add_cog(TF(bot))
