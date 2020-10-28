import discord

from discord.ext import commands

devs = [114348811995840515, 365274392680333329, 372078453236957185]
blacklisted_users = []

class no_perms(commands.MissingPermissions):
    pass

def is_dev():
    def predicate(ctx):
        if ctx.author.id in devs:
            return True
        else:
            raise no_perms(['IS_DEVELOPER'])
    return commands.check(predicate)