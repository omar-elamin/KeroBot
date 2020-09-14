import ast
import discord
import datetime
import os
import time
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
botToken = os.getenv('botToken')

bot = commands.Bot(command_prefix=os.getenv('prefix'), description='Kero Help Command')
devs = [114348811995840515, 365274392680333329, 372078453236957185]
blacklistFile = open(r"blacklist.txt", "r+")
blackList = []
guildsN = []
franNames = ['complex', 'fran']

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
            print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Extensions] {extension} loaded successfully");
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


'''@bot.event
async def on_member_update(before, after):
    botschannel = bot.get_channel(740619681680982109)
    if before.id == 607019207602864198 and after.nick != 'bowie':
        guild = before.guild
        bowieembed = discord.Embed(description=f"Elmon eats ass.",
                                   color=0x0101af)
        await after.edit(nick="bowie")
        await botschannel.send(embed=bowieembed)'''


@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def muteall(ctx, *, vc: discord.VoiceChannel):
    for x in vc.members:
        await x.edit(mute=True)
    await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} muted everyone in {vc.name}', colour=0xbc0a1d))


@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def unmuteall(ctx, *, vc: discord.VoiceChannel):
    for x in vc.members:
        await x.edit(mute=False)
    await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} unmuted everyone in {vc.name}',colour=0xbc0a1d))
    
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
    blacklisted = discord.Embed(description='It appears you were blacklisted by a developer.')
    blacklisted.title = 'Hmm'
    blacklisted.color = 0xFF0000
    blacklisted.set_footer(text="DM any dev (,listdevs) to be unblacklisted.")
    if message.author.id in blackList and message.content.startswith(os.getenv('prefix')):
        await message.channel.send(embed=blacklisted)
        print("[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Blacklist] {} tried running command {}".format(message.author, message.content))
        return
    if isinstance(message.channel, discord.channel.DMChannel):
        dmEmbed = discord.Embed()
        dmEmbed.description = message.content
        dmEmbed.color = 0xbc0a1d
        dmEmbed.set_author(icon_url=message.author.avatar_url, name=message.author.name)
        await bot.get_channel(751885078463774810).send(embed=dmEmbed)
    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} ran: {ctx.message.content} in guild: {ctx.guild.name}')
    loggingchannel = bot.get_channel(751158338821029919)
    randomcolour = "%06x" % random.randint(0, 0xFFFFFF)
    log = discord.Embed(title='Logging', description=f'{ctx.author} ran: {ctx.message.content} in guild: {ctx.guild.name}', colour=discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    await loggingchannel.send(embed=log)
    
@bot.event
async def on_command_error(ctx, error):
    await ctx.send('''```py
{}```'''.format(error))
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Commands] {ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}')
    loggingchannel = bot.get_channel(751158338821029919)
    randomcolour = "%06x" % random.randint(0, 0xFFFFFF)
    log = discord.Embed(title='Error Logging', description=f'{ctx.author} failed running: {ctx.message.content} in guild: {ctx.guild.name}', colour=discord.Colour.from_rgb(255,0,0))
    await loggingchannel.send(embed=log)


@bot.command(pass_context=True)
async def listdevs(ctx):
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the Dev list.')
    devlistMessage = ''
    for x in devs:
        dev = bot.get_user(x)
        devlistMessage += f'- {dev}\n'
    devlistEmbed = discord.Embed(description=devlistMessage, title='Developers:', color = 0xbc0a1d)
    await ctx.send(embed=devlistEmbed)

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
    await ctx.send(embed=discord.Embed(description=f'{ctx.author.name} has shut down the bot.', colour=0xbc0a1d))
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Shutdown] {ctx.author.name}: shutting down {bot.user.name} command sent in {ctx.guild.name}')
    await bot.logout()


@bot.command(pass_context=True, help='Get the link to anyones profile photo!')
async def avatar(ctx, *, member: discord.Member=None):
    if not member: member=ctx.author
    avatarembed = discord.Embed(colour=0xbc0a1d)
    avatarembed.set_image(url=str(member.avatar_url_as(format='png', size=1024)))
    await ctx.send(embed=avatarembed)
    print(f"[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Gave {member}'s avatar to {ctx.author.name}")


@bot.command(pass_context=True)
@commands.check(is_dev)
async def blacklist(ctx, *, user: discord.User):
    blackList.append(user.id)
    await ctx.send(embed=discord.Embed(description=f'{user.name} has been blacklisted.', colour=0xbc0a1d))
    print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Added {user.name} to the blacklist.')


@bot.command(pass_context=True)
@commands.check(is_dev)
async def unblacklist(ctx, *, user: discord.User):
    try:
        await ctx.send(embed=discord.Embed(description=f'{user.name} has been unblacklisted.', colour=0xbc0a1d))
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Removed {user.name} from the blacklist.')
        blackList.remove(user.id)

    except ValueError:
        ctx.send(embed=discord.Embed(description=f'{user.name} is not currently blacklisted.', colour=0xbc0a1d))


@bot.command(pass_context=True)
@commands.check(is_dev)
async def showblacklist(ctx):
    if not blackList:
        await ctx.send(embed=discord.Embed(description='No users currently blacklisted.', colour=0xbc0a1d))
    else:
        print(f'[{datetime.datetime.utcnow().replace(microsecond=0)} INFO]: [Event] Showing {ctx.author.name} the blacklist.')
        blackListMessage = ''
        for x in blackList:
            user = bot.get_user(x)
            blackListMessage += f'- {user.name}\n'
        blackListEmbed = discord.Embed(description=blackListMessage, title='Current blacklist', colour = 0xbc0a1d)
        await ctx.send(embed=blackListEmbed)


@bot.command(pass_context=True)
async def say(ctx, *, msg):
    cmdmsg = ctx.message
    await cmdmsg.delete()
    await ctx.send(f'{msg}')


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(embed=discord.Embed(description=f'Latency: {round(bot.latency * 1000, 2)}ms', colour=0xbc0a1d))

@bot.command(pass_context=True)
async def uptime(ctx):
    command_send_time = datetime.datetime.utcnow()
    uptime = command_send_time - starttime
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(embed=discord.Embed(description=f'Uptime: `{days} days` `{hours} hours` `{minutes} minutes` and `{seconds} seconds.`', colour=0xbc0a1d))


@bot.command(pass_context=True)
@commands.check(is_dev)
async def showguilds(ctx):
    message = ""
    for x in bot.guilds:
        message += f'{x.name} | {len(x.members)} members\n'
    embedGuilds = discord.Embed(description=message, title=f'Guilds [{len(bot.guilds)}]', colour=0xbc0a1d)
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
async def userinfo(ctx, *, user: discord.Member=None):
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

@bot.command(pass_context=True)
async def serverinfo(ctx):
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
    if result is not None:
        await ctx.send(embed=discord.Embed(description=f'{result}', colour=0xbc0a1d))


bot.run(botToken)
