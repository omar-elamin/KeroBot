import os
import discord
from dotenv import load_dotenv
import datetime
from discord.ext import commands
from discord import member
from discord.utils import get
from discord import VoiceClient
import youtube_dl
import time
import ast


load_dotenv()
botToken = os.getenv('botToken')

currentGuild = os.getenv('guildName')
bot = commands.Bot(command_prefix=os.getenv('prefix'), description='description')
devs = [114348811995840515, 365274392680333329, 372078453236957185, 147765181903011840]
blacklistFile = open(r"blacklist.txt", "r+")
blackList = []
client = discord.Client()
guildsN = []

for line in blacklistFile:
    blackList.append(line.strip('\n'))

def is_dev(ctx):
    return(ctx.message.author.id in devs)
starttime = ''

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')
    print(''''\t
    ''')
    game = discord.Game('with your feelings')
    await bot.change_presence(status=discord.Status.online, activity = game)
    
    print('Bot currently in {guildCount} guilds.')
    for guild in bot.guilds:
        print(f'Connected to guild: {guild.name}, Owner: {guild.owner}')
        guildsN.append(guild.name)
    print('\nCurrent blacklist:')
    for x in blackList:
        print(f' - {x}')
    print('\n')
    global starttime
    starttime = datetime.datetime.utcnow()
    
commandNames = ['francisco', '-', 'debug', 'addrole', 'shutdown', 'delrole', 'kick', 'ban', 'avatar', 'music']
textResponses = ['gay']

@bot.command(pass_context=True)
async def listdevs(ctx):
    await ctx.send("Current devs:")
    for x in devs:
        dev = bot.get_user(x)
        await ctx.send(f'- {dev}')
           
#@bot.command(name = commandNames[0])    
#async def francisco(msg):
#    await msg.send(textResponses[0])

@bot.command(pass_context=True)
async def dm(ctx, user: discord.Member,*, msg):
    if (commands.check(is_dev) or user == ctx.author):
        await user.send(msg)
        print(f'sent DM to {user.name}: {msg}')
    
#@bot.command(name = commandNames[2], help='')
#@commands.check(is_dev)
#async def debug(ctx, command, args1: discord.Member, *,args2: discord.Role):
#    if command == 'addrole':
#        guild = discord.Message.guild.name
 #       await args1.add_roles(args2)
  #      await ctx.send(f'Missing permission: manage_roles=True')
   #     print(f"Added: {args2} to: {args1.name} in: {ctx.guild.name} (debug)")
    #elif command == 'delrole':
     #   guild = discord.Message.guild.name
      #  await args1.remove_roles(args2)
       # await ctx.send(f'Missing permission: manage_roles=True')
        #print(f"Removed: {args2} from: {args1.name} in: {ctx.guild.name} (debug)")

@bot.command(name = commandNames[3], help ='Adds a role to a specified user. Usage: ,addrole [user] [role]')
@commands.has_permissions(manage_roles=True)
async def addRole(ctx, user: discord.Member,*, role: discord.Role):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        guild = discord.Message.guild.name
        await user.add_roles(role)
        await ctx.send(f'{user.name} has been assigned the role {role.name} by: {ctx.author.name}')
        print(f"Added: {role} to: {user.name} in: {ctx.guild.name}")
    
@bot.command(name=commandNames[4], help='Shuts down the bot', aliases=['kill', 'restart'])
@commands.check(is_dev)
async def shutdown(ctx):
    blacklistFile.close()
    print('Updating blacklist')
    updatingFile = open(r'blacklist.txt', 'w+')
    for x in blackList:
        updatingFile.write(x+'\n')
    updatingFile.close()
    await ctx.send(f'{ctx.author.name} has shut down the bot.')
    print(f'{ctx.author.name}: shutting down {bot.user.name} command sent in {ctx.guild.name}')
    await bot.logout()
    
@bot.command(name = commandNames[5], help ='Removes a role from a specified user. Usage: ,delrole [user] [role]')
@commands.has_permissions(manage_roles=True)
async def delRole(ctx, user: discord.Member,*, role: discord.Role):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        guild = discord.Message.guild.name
        await user.remove_roles(role)
        await ctx.send(f'{user.name} has been removed from the role {role.name} by: {ctx.author.name}')
        print(f"Removed role: {role} from: {user.name} in: {ctx.guild.name}")

@bot.command(name = commandNames[6], help='Kicks a user from the guild. Usage: ,kick [user] [reason]')
@commands.has_permissions(kick_members=True)
async def kick(ctx, user : discord.Member, *, reason=None):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        guild = discord.Message.guild.name
        await user.kick(reason=f'{reason} || by: {ctx.author.name}')
        await ctx.send(f'{user.name} has been kicked by: {ctx.author.name} for reason: {reason}')
        print(f"Kicked {user.name} from {ctx.guild.name}")
    
@bot.command(name=commandNames[7], help='Bans a user from the guild. Usage: ,ban [user] [reason]')
@commands.has_permissions(ban_members=True)
async def ban(ctx, user : discord.Member, *, reason=None):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        guild = discord.Message.guild.name
        await user.ban(reason=f'{reason} || by: {ctx.author.name}', delete_message_days=0)
        await ctx.send(f'{user.name} has been banned by: {ctx.author.name} for reason: {reason}')
        print(f"Banned {user.name} from {ctx.guild.name}")
    
@bot.command(name=commandNames[8], help='Get the link to anyones profile photo!')
async def avatarFinder(ctx, user : discord.Member):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        avatarurl = str(user.avatar_url)
        await ctx.send(f'{avatarurl}')
        print(f"Gave {user}'s avatar to {ctx.author.name}")

@bot.command(pass_context=True)
@commands.check(is_dev)
async def blacklist(ctx,*, name):
    blackList.append(name)
    await ctx.send(f'{name} has been blacklisted.')
    print(f'Added {name} to the blacklist.')

@bot.command(pass_context=True)
@commands.check(is_dev)
async def unblacklist(ctx,*, name):
    try:
        await ctx.send(f'{name} has been unblacklisted.')
        print(f'Removed {name} from the blacklist.')
        blackList.remove(name)
        
    except ValueError:
        ctx.send(f'{name} is not currently blacklisted.')

    
        
@bot.command(pass_context=True)
@commands.check(is_dev)
async def showblacklist(ctx):
    if not blackList:
        await ctx.send('No players currently blacklisted.')
    else:
        print(f'Showing {ctx.author.name} the blacklist.')
        await ctx.send('Current blacklist:')
        for x in blackList:
            await ctx.send(f' - {x}')

@bot.command(pass_context=True)
async def say(ctx, *, msg):
    if ctx.author.name in blackList:
        return await bot.say('Error: It appears you are blacklisted.')
    else:
        cmdMsg = ctx.message
        await cmdMsg.delete()
        await ctx.send(f'{msg}')

@bot.command(pass_context=True)
async def purge(ctx, msgs):
    channel = ctx.channel
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    elif (commands.has_permissions(manage_messages=True) or commands.check(is_dev)):
        await channel.purge(limit=(int(msgs)+1))
        await ctx.send(f'{ctx.author.name} deleted {msgs} messages')
        print(f'{ctx.author.name} purged {msgs} messages in {ctx.guild.name}')

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'Latency: {round(bot.latency, 2)}ms')

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason='no reason specified'):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(mutedRole)
        await ctx.send(f'{member} muted by: {ctx.author.name} for: {reason}')
        print(f'Muted {member} in {ctx.guild.name}')
    
@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    if ctx.author.name in blackList:
        await ctx.send('It appears you are blacklisted.')
    else:
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(mutedRole)
        await ctx.send(f'{member} unmuted by {ctx.author.name}')
        print(f'Unmuted {member} in {ctx.guild.name}')



@bot.command(pass_context=True)
async def uptime(ctx):
    command_send_time = datetime.datetime.utcnow()
    uptime = command_send_time - starttime
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f'Uptime: **{days}** days, **{hours}** hours, **{minutes}** minutes, and **{seconds}** seconds.')

@bot.command(pass_context=True)
async def nick(ctx, user: discord.Member,*, nick):
    if (commands.has_permissions(manage_nicknames=True) or ctx.author.name == elmon):
        await user.edit(nick=nick)

@bot.event
async def on_member_update(before, after):
    botschannel = bot.get_channel(740619681680982109)
    if before.id == 607019207602864198 and after.nick != 'belle delphine':
        bowieEmbed = discord.Embed(description="Changed bowie's name back to belle delphine <@653719710147411969>", color=0x00ff00)
        await after.edit(nick="belle delphine")
        await botschannel.send(embed=bowieEmbed)
            
@bot.command(pass_context=True)
@commands.check(is_dev)
async def showguilds(ctx):
    message=""
    for x in bot.guilds:
        message += f'{x.name} | {len(x.members)} members\n'   
    embedGuilds = discord.Embed(description=message, title=f'Guilds [{len(bot.guilds)}]')
    await ctx.send(embed=embedGuilds)
            
franNames = ['complex', 'fran', 'francisco']
@bot.event
async def on_message(message):
    if message.author.name == bot.user.name:
        print('ingoring self message')
    else:
        channel = message.channel
        #  Guild specific features
        if channel.guild.name == 'resonance':
            pass
        if channel.guild.name == 'Kero':
            for x in franNames:
                if (x in (message.content).lower()):
                    await channel.send('Fran is a homosexual.')
        if channel.guild.name == 'Radical Roller Rink':
            if '!rank' in message.content and channel.name != 'bot-spam':
                await channel.send('<#741113645487882381>')
                time.sleep(1)
                await channel.purge(limit=1)
        await bot.process_commands(message)

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
    messagetoSend=f'''`Username:` {user.name}
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
async def debug(ctx, *, cmd):
    """Evaluates input.
    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.
    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function
    Such that `>eval 1 + 1` gives `2` as the result.
    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating
    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
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
    await ctx.send(result)

bot.run(botToken)
