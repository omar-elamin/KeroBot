import ast
import discord
import datetime
import os
import time

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
botToken = os.getenv('botToken')

currentGuild = os.getenv('guildName')
bot = commands.Bot(command_prefix=os.getenv('prefix'), description='Kero Help Command')
devs = [114348811995840515, 365274392680333329, 372078453236957185, 147765181903011840]
blacklistFile = open(r"blacklist.txt", "r+")
blackList = []
guildsN = []
franNames = ['complex', 'fran', 'francisco']

for line in blacklistFile:
    blackList.append(int(line.strip('\n')))

def is_dev(ctx):
    return ctx.message.author.id in devs


starttime = ''

extensions = [
    "commands.moderation",
    "commands.music"
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Extensions] {extension} loaded successfully")
        except Exception as e:
            print("[{} INFO]: [Extensions] {} didn't load {}".format(datetime.datetime.utcnow().replace(microsecond=0), extension, e))


@bot.event
async def on_ready():
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Client] {bot.user.name} is online.')
    game = discord.Game('with your feelings')
    await bot.change_presence(status=discord.Status.online, activity=game)

    guildCount = len(bot.guilds)
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Guilds] Bot currently in {guildCount} guilds.')
    for guild in bot.guilds:
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Guilds] Connected to guild: {guild.name}, Owner: {guild.owner}')
        guildsN.append(guild.name)
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] Current blacklist:')
    for x in blackList:
        user = bot.get_user(x)
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] - {user.name}')
    global starttime
    starttime = datetime.datetime.utcnow()


@bot.event
async def on_member_update(before, after):
    botschannel = bot.get_channel(740619681680982109)
    if before.id == 607019207602864198 and after.nick != 'belle delphine':
        guild = before.guild
        bowieembed = discord.Embed(description=f"Changed bowie's name back to belle delphine in {before.guild.name} <@653719710147411969>",
                                   color=0x00ff00)
        await after.edit(nick="belle delphine")
        await botschannel.send(embed=bowieembed)


@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def muteall(ctx, voicechannel):
    vc = discord.utils.get(ctx.guild.voice_channels, name=voicechannel)
    for x in vc.members:
        await x.edit(mute=True)
    await ctx.send(f'`{ctx.author.name}` muted everyone in `{vc.name}`')
    
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def unmuteall(ctx, voicechannel):
    vc = discord.utils.get(ctx.guild.voice_channels, name=voicechannel)
    for x in vc.members:
        await x.edit(mute=False)
    await ctx.send(f'`{ctx.author.name}` unmuted everyone in `{vc.name}`')
    
@bot.event
async def on_message(message):
    if message.author.name == bot.user.name:
        return
    else:
        channel = message.channel
        #  Guild specific features
        if isinstance(message.channel, discord.channel.DMChannel):
            pass
        else:
            if channel.guild.name == 'Kero':
                for x in franNames:
                    if x in message.content.lower():
                        await channel.send('Fran is a homosexual.')
            if channel.guild.name == 'Radical Roller Rink':
                if '!rank' in message.content and channel.name != 'bot-spam':
                    await channel.send('<#741113645487882381>')
                    time.sleep(1)
                    await channel.purge(limit=1)
            await bot.process_commands(message)
    blacklisted = discord.Embed(description='It appears you were blacklisted by a developer.')
    if message.author.id in blackList and message.content.startswith(os.getenv('prefix')):
        await message.channel.send(embed=blacklisted)
        print("[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] {} tried running command {}".format(message.author, message.content))
        return
    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} ran: {ctx.message.content} in guild: {ctx.guild.name}')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send("Error while running command: `{}`".format(error))
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}')

textResponses = ['gay']


@bot.command(pass_context=True)
async def listdevs(ctx):
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the Dev list.')
    devlistMessage = ''
    for x in devs:
        dev = bot.get_user(x)
        devlistMessage += f'- {dev}\n'
    devlistEmbed = discord.Embed(description=devlistMessage, title='Developers:')
    await ctx.send(embed=devlistEmbed)


# @bot.command()
# async def francisco(msg):
#    await msg.send(textResponses[0])

@bot.command(pass_context=True)
async def dm(ctx, user: discord.Member, *, msg):
    if commands.check(is_dev) or user == ctx.author:
        await user.send(msg)
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] sent DM to {user.name}: {msg}')


@bot.command(help='Shuts down the bot', aliases=['kill', 'restart'])
@commands.check(is_dev)
async def shutdown(ctx):
    blacklistFile.close()
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] Updating blacklist')
    updatingFile = open(r'blacklist.txt', 'w+')
    for x in blackList:
        updatingFile.write(str(x) + '\n')
    updatingFile.close()
    await ctx.send(f'{ctx.author.name} has shut down the bot.')
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Shutdown] {ctx.author.name}: shutting down {bot.user.name} command sent in {ctx.guild.name}')
    await bot.logout()


@bot.command(help='Get the link to anyones profile photo!')
async def avatar(ctx, member: discord.Member):
    avatarurl = str(member.avatar_url)
    await ctx.send(f'{avatarurl}')
    print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Gave {member}'s avatar to {ctx.author.name}")


@bot.command(pass_context=True)
@commands.check(is_dev)
async def blacklist(ctx, *, user: discord.User):
    blackList.append(user.id)
    await ctx.send(f'{user.name} has been blacklisted.')
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Added {user.name} to the blacklist.')


@bot.command(pass_context=True)
@commands.check(is_dev)
async def unblacklist(ctx, *, user: discord.User):
    try:
        await ctx.send(f'{user.name} has been unblacklisted.')
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Removed {user.name} from the blacklist.')
        blackList.remove(user.id)

    except ValueError:
        ctx.send(f'{user.name} is not currently blacklisted.')


@bot.command(pass_context=True)
@commands.check(is_dev)
async def showblacklist(ctx):
    if not blackList:
        await ctx.send('No users currently blacklisted.')
    else:
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the blacklist.')
        blackListMessage = ''
        for x in blackList:
            user = bot.get_user(x)
            blackListMessage += f'- {user.name}\n'
        blackListEmbed = discord.Embed(description=blackListMessage, title='Current blacklist')
        await ctx.send(embed=blackListEmbed)


@bot.command(pass_context=True)
async def say(ctx, *, msg):
    cmdmsg = ctx.message
    await cmdmsg.delete()
    await ctx.send(f'{msg}')


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'Latency: {round(bot.latency * 1000, 2)}ms')


@bot.command(pass_context=True)
async def uptime(ctx):
    command_send_time = datetime.datetime.utcnow()
    uptime = command_send_time - starttime
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f'Uptime: `{days} days` `{hours} hours` `{minutes} minutes` and `{seconds} seconds.`')


@bot.command(pass_context=True)
@commands.check(is_dev)
async def showguilds(ctx):
    message = ""
    for x in bot.guilds:
        message += f'{x.name} | {len(x.members)} members\n'
    embedGuilds = discord.Embed(description=message, title=f'Guilds [{len(bot.guilds)}]')
    await ctx.send(embed=embedGuilds)


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command(pass_context=True)
async def userinfo(ctx, *, user: discord.Member):
    messagetoSend = f'''`Username:` {user.name}
`Discriminator:` {user.discriminator}
`Nickname:` {user.nick}
`ID:` {user.id}
`Avatar URL:` `{user.avatar_url}`
`Status:` {user.status}
`Activity:` {user.activity}
`Bot?` {user.bot}
`Account Created On:` {user.created_at}
`Account Guild Join Date:` {user.joined_at}
`On a Phone?` {user.is_on_mobile()}'''
    await ctx.send(messagetoSend)


@bot.command(name='eval')
@commands.check(is_dev)
async def debug(ctx, *, cmd):
    #Evaluates input.
    #Input is interpreted as newline seperated statements.
    #If the last statement is an expression, that is the return value.
    #Usable globals:
    #  - `bot`: the bot instance
    #  - `discord`: the discord module
    #  - `commands`: the discord.ext.commands module
    #  - `ctx`: the invokation context
    #  - `__import__`: the builtin `__import__` function
    #Such that `>eval 1 + 1` gives `2` as the result.
    #The following invokation will cause the bot to send the text '9'
    #to the channel of invokation and return '3' as the result of evaluating
    #>eval ```
    #a = 1 + 2
    #b = a * 2
    #await ctx.send(a + b)
    #a
    #```
    
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(f'`{result}`')


bot.run(botToken)
