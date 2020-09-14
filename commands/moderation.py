import discord

from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user: discord.Member, *, role: discord.Role):
        """Adds a role to a specified user."""
        await user.add_roles(role)
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been assigned the role {role.name} by: {ctx.author.name}', colour=0xbc0a1d))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Added: {role} to: {user.name} in: {ctx.guild.name}")
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx, user: discord.Member, *, role: discord.Role):
        """Removes a role from a specified user."""
        await user.remove_roles(role)
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been removed from the role {role.name} by: {ctx.author.name}', colour=0xbc0a1d))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Removed role: {role} from: {user.name} in: {ctx.guild.name}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """Kicks a user from the guild."""
        await user.kick(reason=f'{reason} || by: {ctx.author.name}')
        await ctx.send(embed=discord.Embed(embed=f'{user.name} has been kicked by: {ctx.author.name} for reason: {reason}', colour=0xbc0a1d))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Kicked {user.name} from {ctx.guild.name}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """Bans a user from the guild."""
        await user.ban(reason=f'{reason} || by: {ctx.author.name}', delete_message_days=0)
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been banned by: {ctx.author.name} for reason: {reason}',colour=0xbc0a1d))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Banned {user.name} from {ctx.guild.name}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason=None):
        await ctx.guild.unban(user, reason=f'{reason} || by: {ctx.author.name}')
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been unbanned by: {ctx.author.name} for reason: {reason}', colour=0xbc0a1d))
        print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Banned {user.name} from {ctx.guild.name}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, msgs):
        """Purge messages from a channel."""
        channel = ctx.channel
        await channel.purge(limit=(int(msgs) + 1))
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} deleted {msgs} messages',colour=0xbc0a1d))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] {ctx.author.name} purged {msgs} messages in {ctx.guild.name}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=''):
        """Mutes a member of the server."""
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        if mutedrole is None:
            return await ctx.send(embed=discord.Embed(description="Role Muted doesn't exist", colour=0xbc0a1d))
        await member.add_roles(mutedrole, reason = f'{reason} || by {ctx.author.name}')
        if reason == '':
            reason = 'no reason specified'
        await ctx.send(embed=discord.Embed(description=f'{member} muted by: {ctx.author.name} for: {reason}', colour=0xbc0a1d))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Moderation] Muted {member} in {ctx.guild.name}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=''):
        """Unmutes a member of the server."""
        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        if mutedrole is None:
            mutedrole = discord.utils.get(ctx.guild.roles, name='muted')
            if mutedrole is None:
                return await ctx.send(embed=discord.Embed(description="Role Muted doesn't exist", colour=0xbc0a1d))
        await member.remove_roles(mutedrole, reason = f'{reason} || by {ctx.author.name}')
        await ctx.send(embed=discord.Embed(description=f'{member} unmuted by {ctx.author.name}', colour=0xbc0a1d))
        print(f'[Moderation] Unmuted {member} in {ctx.guild.name}')

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, user: discord.Member, *, nick):
        await user.edit(nick=nick)
        await ctx.send(embed=discord.Embed(description=f'Changed {user}\'s nickname to {nick}',colour=0xbc0a1d))


def setup(bot):
    bot.add_cog(Moderation(bot))
