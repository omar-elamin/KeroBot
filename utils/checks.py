import discord

from discord.ext import commands
from utils import functions

devs = [114348811995840515, 365274392680333329, 372078453236957185]
blacklisted_users = []
nodm_ids = []
dj_roles = functions.read_json('dj_roles')


class no_perms(commands.MissingPermissions):
    pass

def is_dev():
    def predicate(ctx):
        if ctx.author.id in devs:
            return True
        else:
            raise no_perms(['IS_DEVELOPER'])
    return commands.check(predicate)

def is_fran_or_perms():
    def predicate(ctx):
        if ctx.author.id == 328126114801385472 or commands.has_permissions(kick_members=True):
            return True
        raise no_perms(['MUTE_VOICECHANNEL_MEMBERS'])
    return commands.check(predicate)

def is_tf_and_perms():
    def predicate(ctx):
        if ctx.guild.id == 769659653096472627:
            user = ctx.message.author
            for role in user.roles:
                if role.id in [769659653121900553, 769659653129896016]:
                    return True
        else:
            raise no_perms(['IS_STAFF_MEMBER'])
    return commands.check(predicate)

def is_dj():
    def predicate(ctx):
        guild_key = str(ctx.guild.id)
        for role in ctx.author.roles:
            if role.id == int(dj_roles[guild_key]):
                return True
        raise no_perms(['IS_DJ'])
    return commands.check(predicate) 
