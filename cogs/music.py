import discord
from cogs.lib.youtube_dl_mod import YoutubeDL
from discord.ext import commands
from discord import app_commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.playing = False
        self.paused = False
        self.ytdlOPTS = {'format': 'bestaudio','noplaylist': True,'quiet': True}
        self.FFmpegOPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    
    # Checks
    async def play_checks(self,ctx):
        bot = ctx.guild.get_member(self.bot.user.id)
        if ctx.author.voice == None:
            raise Exception('User not in voice chat')
        if (bot.voice == None) or (bot.voice.channel != self.vc):
            self.voice = await ctx.author.voice.channel.connect()
            return
        if (bot.voice.channel == ctx.author.voice.channel):
            return
    def disconnect_checks(self,ctx):
        bot = ctx.guild.get_member(self.bot.user.id)
        if (bot.voice.channel == None):
            raise Exception('Not in a voice channel to begin with')
        else:
            return

    # Functions
    def searchyt(self,term,mode='normal'):
        with YoutubeDL(self.ytdlOPTS) as ytdl:
            match mode:
                case 'normal': 
                    try:
                        vid = ytdl.extract_info('ytsearch:%s' % term, download=False)['entries'][0]
                    except: return
                    info = {'url': vid['formats'][0]['url'], 'title': vid['title']}
                case 'choice':
                    info = {}
                    for i in range(5):
                        try:
                            vid = ytdl.extract_info('ytsearch:%s' % term, download=False)['entries'][i]
                        except: return
                        iterinfo= {i:{'url': vid['formats'][i]['url'],'title': vid['title']}}
                        info.append(iterinfo)
            return info
    def queuemanage(self,ctx):
        if not len(self.queue) > 0:
            self.playing = False
            return
        self.playing = True
        self.nowplaying = self.queue[0]['title']
        song = self.queue[0]['url']
        self.queue.pop(0)
        self.voice.play(discord.FFmpegPCMAudio(source=song,**self.FFmpegOPTS),after=lambda e:self.queuemanage(ctx))
    
    # Commands
    @commands.hybrid_command(name='play',description='Play a song from YouTube.',aliases=['paly','pla','p'])
    @app_commands.describe(term='Search term or link to the song.')
    async def play(self,ctx,term):
        # Check handling
        self.vc = ctx.author.voice.channel
        try:
            await self.play_checks(ctx)
        except Exception as e:
            match str(e):
                case 'User not in voice chat':
                    await ctx.send(f'{ctx.author.mention}, you are not in a voice channel!')
                case _:
                    await ctx.send('An unknown error occurred. Please try again.')
                    print(e)
            return
        await ctx.send(f'Searching `{term}` on YouTube...')
        self.queue.append(self.searchyt(term=term))
        await ctx.send('Added `{title}` to queue!'.format(title=self.queue[0]['title']))
        if self.playing != True:
            self.queuemanage(ctx.channel)
        else: pass

    @commands.hybrid_command(name='disconnect',aliases=['stop','d','sotp'],description='Disconnects the bot from the voice channel and clears the queue.')    
    async def disconnect(self,ctx):
        # Check handling
        try:
            self.disconnect_checks(ctx)
        except Exception as e:
            match str(e):
                case 'Not in a voice channel to begin with':
                    await ctx.send('Can\'t disconnect if I wasn\'t connected in the first place!')
                    return
                case _:
                    await ctx.send('An unknown error has occurred. Please try again.')
                    print(e)
                    return
        self.voice.stop()
        self.queue = []
        await self.vc.disconnect()
        await ctx.send('Disconnected from the voice channel and cleared the queue!')

    @commands.hybrid_command(name='skip',aliases=['sikp','spki','s'],description='Skips the current song.')
    async def skip(self,ctx):
        if not((self.vc != None) and self.playing == True):
            await ctx.send('I can\'t skip a non-existent song you moron!')
            return
        await self.voice.stop()
        await ctx.send(f'Skipped {self.nowplaying}')
        self.queuemanage(ctx)
            

    @commands.hybrid_command(name='queue',aliases=['np','q','now_playing','list','l'],description='Shows the curent queue.')
    async def music_queue(self,ctx):
        if not self.playing == True:
            await ctx.send('The queue is empty.')
            return
        titles = '\n'.join([i['title'] for i in self.queue])
        queue_embed = discord.Embed(
            color=0x1770fe,
            title='Queue'
        )
        queue_embed.add_field(name='Now playing:',value=self.nowplaying+'\n',inline=False)
        if len(self.queue) > 0:
            queue_embed.add_field(name='Queued songs:',value=titles,inline=False)
        await ctx.send(embed=queue_embed)

async def setup(bot):
    await bot.add_cog(Music(bot))