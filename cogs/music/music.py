import discord
import datetime
import lavalink
import re
import random

from utils import functions
from utils import checks
from discord.ext import commands

url_rx = re.compile(r'https?://(?:www\.)?.+')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(723524131970351194)
        self.bot.music.add_node('localhost', 8888, [CENSORED], 'eu', 'music_node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)
        
    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)
    
    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
    
    async def disconnect_from(self, guild_id: int):
        ws = self.bot._connection.voice_clients    

    @commands.command()
    async def join(self, ctx):
        'Join the voice channel.'
        em = discord.Embed()
        em.title = 'Music'
        em.colour = 0xbc0a1d
        vc = ctx.author.voice.channel
        member = ctx.author
        if member is not None and member.voice is not None:
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))
                em.description = f'Joined {vc.name}'
        else:
            em.description = f'No VC Found.'
        await ctx.send(embed=em)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query):
        'Play a song'
        em = discord.Embed()
        em.title = 'Music'
        em.colour = 0xbc0a1d
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            query = query.strip('<>')
            if not url_rx.match(query):
                query = f'ytsearch:{query}'
            
            results = await player.node.get_tracks(query)
            if not results or not results['tracks']:
                em.description = 'No results found.'
                
            elif results['loadType'] == 'PLAYLIST_LOADED':
                tracks = results['tracks']
    
                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)
    
                em.description = f'Added playlist: {results["playlistInfo"]["name"]} - {len(tracks)} tracks'
            else:
                track = results['tracks'][0]
                em.description = f'Added song: [{track["info"]["title"]}]({track["info"]["uri"]})'
    
                track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
                player.add(requester=ctx.author.id, track=track)
        except Exception as e:
            em.description = f'Error while playing : {e}'
         
        em.colour = 0xbc0a1d
        await ctx.send(embed=em)
        
        if not player.is_playing:
            await player.play()
   
    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        'Get all the songs in the queue'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        em = discord.Embed()
        em.title = 'Queue'
        em.colour = 0xbc0a1d
        if player.current:
            now_playing = player.current.title
            em.add_field(name='Now playing', value=now_playing, inline=False)
            queue_info = ''
            for index in range(len(player.queue)):
                queue_info += f'{index+1}. {player.queue[index].title}\n'
            if queue_info:
                em.add_field(name='Queue', value=queue_info, inline=False)
        else:
            em.description = 'Nothing currently playing.'
        await ctx.send(embed=em)

    @commands.command(aliases=['np'])
    async def nowplaying(self,ctx):
        'Get the currently playing song'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        em = discord.Embed()
        em.title = 'Now playing...'
        em.colour = 0xbc0a1d
        if player.current:
            now_playing = player.current.title
            em.add_field(name='Now playing', value=now_playing, inline=False)
        else:
            em.description = 'Nothing currently playing.'
        
        await ctx.send(embed=em)
    
    @checks.is_dj()
    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        'Get all the songs in the queue'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        em = discord.Embed()
        em.title = 'Music'
        em.colour = 0xbc0a1d
        
        em.description = f'Skipped {player.current.title}'
        await player.skip()
        await ctx.send(embed=em)
    
    @checks.is_dj()
    @commands.command(aliases=['dc','disconnect', 'stop'])
    async def leave(self, ctx):
        'Leave the VC'
        em = discord.Embed()
        em.title = 'Music'
        em.colour = 0xbc0a1d
        player = self.bot.music.player_manager.get(ctx.guild.id)
        
        if not player.is_connected:
            em.description = 'Cannot leave if I was never connected.'
        
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            em.description = 'Must be in the same VC as the bot to disconnect it.'
        
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        
        em.description = 'Disconnected.'
        
        await ctx.send(embed=em)
    
    @checks.is_dj()
    @commands.command(aliases=['v'])
    async def volume(self, ctx, volume:int):
        'Manage the volume'
        em = discord.Embed()
        em.colour = 0xbc0a1d
        em.title='Music'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if not volume or volume > 150:
            em.description = f'Current volume: {player.volume}'
        else:      
            await player.set_volume(volume)
            em.description = f'Set the volume to: {player.volume}'
        await ctx.send(embed=em)
    
    @checks.is_dj()
    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        'Pauses the player'
        em = discord.Embed()
        em.colour = 0xbc0a1d
        em.title='Music'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        await player.set_pause(not player.paused)
        if player.paused:
            em.description = 'Player paused'
            em.colour = 0xFF0000
        else:
            em.description = 'Player resumed'
            em.colour = 0x00FF00
        await ctx.send(embed=em)
    
    @checks.is_dj()
    @commands.command(aliases=['mix'])
    async def shuffle(self, ctx):
        'Shuffle the queue'
        em = discord.Embed()
        em.title='Shuffled'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        random.shuffle(player.queue)
        em.colour = 0xbc0a1d
        if player.current:
            now_playing = player.current.title
            em.add_field(name='Now playing', value=now_playing, inline=False)
            queue_info = ''
            for index in range(len(player.queue)):
                queue_info += f'{index+1}. {player.queue[index].title}\n'
            if queue_info:
                em.add_field(name='Queue', value=queue_info, inline=False)
        else:
            em.description = 'Nothing currently playing.'
        await ctx.send(embed=em)
    
    @checks.is_dj()
    @commands.command(aliases=['l', 'repeat'])
    async def loop(self, ctx):
        'Toggle loop'
        em = discord.Embed()
        em.title='Music'
        player = self.bot.music.player_manager.get(ctx.guild.id)
        player.repeat = not player.repeat
        if player.repeat:
            em.description = 'Loop on'
            em.colour = 0x00FF00
        else:
            em.description = 'Loop off'
            em.colour = 0xbc0a1d
        await ctx.send(embed=em)

    @checks.is_dj()
    @commands.command()
    async def earrape(self, ctx): 
        player = self.bot.music.player_manager.get(ctx.guild.id) 
        await player.set_volume(1000)
    
    @checks.is_dj()
    @commands.command(aliases=['goto'])
    async def seek(self, ctx, position):
        'Go to a position in the track in seconds'
        em = discord.Embed()
        em.title='Seeked'
        em.colour = 0xbc0a1d
        if ':' in position:
            temp = position.split(':')
            position = int(f'{(int(temp[0])*60)+int(temp[1])}')
        else:
            position = int(position)
            
        player = self.bot.music.player_manager.get(ctx.guild.id) 
        await player.seek(position*1000)
        if position%60 < 9:
            newpos = f'{position//60}:0{position%60}'
        else:
            newpos = f'{position//60}:{position%60}'
        em.description = f'Skipped to {newpos}'
        await ctx.send(embed=em)
    
    @commands.command(aliases=['djrole'])
    @commands.has_permissions(administrator=True)
    async def setdj(self, ctx, role: discord.Role):
        dj_roles = functions.read_json('dj_roles')
        dj_roles[str(ctx.guild.id)] = str(role.id)
        functions.write_json('dj_roles', dj_roles)
        em = discord.Embed()
        em.title = 'DJ Role'
        em.description = f'Set to: {role.name}'
        em.colour = 0xbc0a1d
        
        await ctx.send(embed=em)
        
    
def setup(bot):
    bot.add_cog(Music(bot))
