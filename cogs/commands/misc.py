import discord
import datetime

from utils import checks
from discord.ext import commands
from utils import functions
from cogs import events

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def listdevs(self, ctx):
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the Dev list.')
        devlistMessage = ''
        for dev_id in checks.devs:
            dev = self.bot.get_user(dev_id)
            devlistMessage += f'- {dev}\n'
        devlistEmbed = discord.Embed(description=devlistMessage, title='Developers:', color = 0xbc0a1d)
        await ctx.send(embed=devlistEmbed)
    
    @commands.command(pass_context=True)
    async def dm(self, ctx, user: discord.Member, *, msg):
        'Send a DM Anonymously (OPT-OUT USING ,nodm)'
        if user.id not in checks.nodm_ids:
            em = discord.Embed(title='Anonymous message', description=msg)
            await user.send(embed=em)
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] {ctx.author} sent anonymous DM to {user.name}: {msg}')
        else:
            em = discord.Embed(title='Not sent.', description='That user has opted out of Anonymous DMs.')
            await ctx.send(embed=em)
            
    @commands.command()
    async def invite(self, ctx):
        "Get the invite link to the bot"
        em = discord.Embed()
        em.title = 'Bot Invite Link'
        em.color = 0xbc0a1d
        invite_url = 'https://discord.com/api/oauth2/authorize?client_id=723524131970351194&permissions=8&scope=bot'
        em.description = f'[Click To Invite]({invite_url})'
        await ctx.send(embed=em)
    
    @commands.command()
    async def nodm(self, ctx):
        'Opt-out of recieving anonymous DMs from the bot.'
        user = ctx.message.author
        if user.id not in checks.nodm_ids:
            checks.nodm_ids.append(user.id)
            data = functions.read_json('nodm')
            data['nodm'].append(user.id)
            functions.write_json('nodm',data)
            await ctx.send(embed=discord.Embed(title='DMs', description=f'You have opted out of Anonymous DMs.', colour=0xbc0a1d))
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Added {user.name} to the No-DM list.')
        else:
            checks.nodm_ids.remove(user.id)
            data = functions.read_json('nodm')
            data['nodm'].remove(user.id)
            functions.write_json('nodm',data)
            await ctx.send(embed=discord.Embed(title='DMs', description=f'You have opted in to Anonymous DMs.', colour=0xbc0a1d))
            print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Removed {user.name} from the No-DM list.')
        
    @commands.command(pass_context=True, help='Get the link to anyones profile photo!', aliases=['av','profile', 'picture'])
    async def avatar(self, ctx, *, member: discord.Member=None):
        if not member: member=ctx.author
        avatarembed = discord.Embed(colour=0xbc0a1d)
        avatarembed.set_image(url=str(member.avatar_url_as(format='png', size=1024)))
        await ctx.send(embed=avatarembed)
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Gave {member}'s avatar to {ctx.author.name}")
    
    @commands.command(pass_context=True)
    async def say(self, ctx, *, msg):
        cmdmsg = ctx.message
        #if '@everyone' in cmdmsg.content or '@here' in cmdmsg.content:
            #msg.replace('@everyone', '[MENTIONED EVERYONE]')
        if cmdmsg.role_mentions:
            index = msg.find('@')
            msg = msg[:index] + '\\'+ msg[index:]
        await ctx.send(f'{msg}')
        try:
            await cmdmsg.delete()
        except:
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Say] Failed to delete a message.")
    
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(description=f'Latency: {round(self.bot.latency * 1000, 2)}ms', colour=0xbc0a1d))
    
    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        command_send_time = datetime.datetime.utcnow()
        uptime = command_send_time - events.starttime
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(embed=discord.Embed(description=f'Uptime: `{days} days` `{hours} hours` `{minutes} minutes` and `{seconds} seconds.`', colour=0xbc0a1d))
    
    @commands.command(pass_context=True)
    async def userinfo(self, ctx, *, user: discord.Member=None):
        if not user: user=ctx.author
        messagetoSend = discord.Embed(title=f'User Information: {user}', color=0xbc0a1d)
        messagetoSend.set_thumbnail(url=user.avatar_url)
        messagetoSend.add_field(name='Username', value = f'{user.name}')
        messagetoSend.add_field(name='Discriminator', value = f'{user.discriminator}')
        messagetoSend.add_field(name='Nick', value = f'{user.nick}')
        messagetoSend.add_field(name='ID', value = f'{user.id}')
        messagetoSend.add_field(name='Avatar URL', value = f'{user.avatar_url}')
        messagetoSend.add_field(name='Status', value = f'{user.status}')
        messagetoSend.add_field(name='Activity', value = f'{user.activity}')
        messagetoSend.add_field(name='Bot?', value = f'{user.bot}')
        messagetoSend.add_field(name='Account Creation Date', value = f'{user.created_at}')
        messagetoSend.add_field(name='Guild Join Date', value = f'{user.joined_at}')
        messagetoSend.add_field(name='On a Phone?', value = f'{user.is_on_mobile()}')
        await ctx.send(embed=messagetoSend)
    
    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        messagetoSend = discord.Embed(title='Server Information', color=0xbc0a1d)
        messagetoSend.set_thumbnail(url=guild.icon_url_as(format='png'))
        messagetoSend.add_field(name='Name', value = f'{guild.name}')
        messagetoSend.add_field(name='ID', value = f'{guild.id}')
        messagetoSend.add_field(name='Description', value = f'{guild.description}')
        messagetoSend.add_field(name='Region', value = f'{guild.region}')
        messagetoSend.add_field(name='Owner', value = f'{guild.owner}')
        messagetoSend.add_field(name='Members', value = f'{guild.member_count}')
        messagetoSend.add_field(name='Guild Creation Date', value = f'{guild.created_at}')
        messagetoSend.add_field(name='Role Count', value = f'{len(guild.roles)}')
        messagetoSend.add_field(name=f'Channel Count ({len(guild.channels)} Total)', value = f'{len(guild.voice_channels)} voice, {len(guild.text_channels)} text')
        messagetoSend.add_field(name='Boost Level', value = f'{guild.premium_tier}')
        messagetoSend.add_field(name='AFK Timeout', value = f'{guild.afk_timeout/60} minutes')
        messagetoSend.add_field(name='AFK Channel', value = f'{guild.afk_channel}')
        await ctx.send(embed=messagetoSend)

def setup(bot):
    bot.add_cog(Misc(bot))
