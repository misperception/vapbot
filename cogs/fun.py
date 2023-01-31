import random, asyncio, discord
from cogs.lib.vapbotutils import ParseUtils
import pandas as pd
from discord.ext import commands
from discord import app_commands
with open("copypasta.txt",'r', encoding='utf-8') as texten:
  copypasta = texten.read()
with open("copypastaes.txt",'r', encoding='utf-8') as textes:
  copypastaes = textes.read()

class Fun(commands.Cog):
    def __init__(bot, self):
        self.bot = bot
    
    @commands.hybrid_command(name='vapcopy', description='Vaporeon copypasta.')
    async def copyp(self, ctx):
        await ctx.send(copypasta)

    @commands.hybrid_command(name='vapcopyes', description='Copypasta de Vaporeon.')
    async def copypes(self, ctx):
        await ctx.send(copypastaes)

    @commands.hybrid_command(name='vapthird', description='[NSFW] 33%% chance of getting an image with one of e621.net\'s ratings.')
    @app_commands.describe(tag="One of the available tags, if any. Write 'help' to see the list.")
    async def oneinthree(self, ctx, tag='none'):

        if not ctx.channel.is_nsfw(): # terminates command if not in a NSFW channel
            await ctx.send('Make sure to run this command on a NSFW channel.')
            return
        value = random.randint(1,3)
        tags = ''
        # executes code based on output number
        rating = ['s','q','e'][value-1]
        dict_tag = pd.read_csv('tags.csv').to_dict(orient='list')
        dict_aliases = pd.read_csv('alias.csv').to_dict(orient='list')

        try:
            t = dict_tag.get(tag)
            tags = rating + t[0] # addition of dict_tag tags according to the argument provided (if at all)
        except:
            try:
                a = dict_aliases.get(tag)
                tags = rating + a[0] # checks for aliases 
            except:
                if tag != 'help':
                    await ctx.send(f'{tag} is not a valid tag, please make sure you are using one of the valid tags')
                    return
                else:
                    await ctx.send('Tags:')
                    await ctx.send(f'``{dict_tag}``')
                    return
        if rating == 'e':
            tags+= '-young'
                    
        endpoint = f'https://e621.net/posts/random.json?tags=rating%3A{tags}'
        await ParseUtils.EmbedMaker(endpoint, ctx)

class Faith_In_Humanity(commands.Cog, name='Faith in humanity'):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='eyebleach', description='Restores a small part of your faith in humanity.')
    async def eyebleach(self, ctx):
        endpoint = "https://e621.net/posts/random.json?tags=vaporeon+rating:safe+-breasts"
        try:
            await ParseUtils.EmbedMaker(endpoint,ctx)
        except:
            await ctx.send("For whatever reason, *ahem, ahem, check the console* the image couldn't be sent. Sucks to be you, huh?")

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    party = []
    mode = ''
    partyCreation = False
    sessionOngoing = False
    sessionMaster: discord.Member

    async def RouletteMain(ctx):
        roundn = 1

        class Actions(discord.ui.View):
            user : discord.User
            shot = False
            spinned = False
            @discord.ui.button(label='Shoot!',style=discord.ButtonStyle.danger)
            async def shoot(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.user != interaction.user:
                    await interaction.response.send_message('It\'s not your turn buddy',ephemeral=True,delete_after=0.8)
                else:
                    self.shot = True
                    await interaction.response.send_message('*click*',ephemeral=True,delete_after=0.8)
                    self.stop()
            
            if Roulette.mode == 'hard':
                @discord.ui.button(label='Spin',style=discord.ButtonStyle.primary)
                async def spin(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.user != interaction.user:
                        await interaction.response.send_message('It\'s not your turn buddy',ephemeral=True,delete_after=0.8)
                    else:
                        await interaction.response.send_message('Spinned the barrel.')
                        self.spinned = True
                        self.spin.disabled = True
                        await self.message.edit(view=self)
            
            async def disable(self):
                for child in self.children:
                    child.disabled = True
                await self.message.edit(view=self)

        async def post(ctx, mode='normal'):
            degentags = ["watersports", "omorashi", "scat", "gore", "vore", "anal_prolapse", "anal_vore", "diaper", "intersex+breasts", "ear_penetration", "fart"]
            endpoint = {
                'normal': 'https://e621.net/posts/random.json?tags=rating:e+-young',
                'degen': 'https://e621.net/posts/random.json?tags=rating:e+-young{tags}'.format(tags='+' + degentags[random.randrange(1,len(degentags))])
            }

            await ParseUtils.EmbedMaker(endpoint.get(mode),ctx.channel)

        HardModeR1 = random.randint(1,6)
        HardModeR2 = random.randint(1,6)
        await ctx.send('Starting the session...')
        await asyncio.sleep(1)
        while Roulette.sessionOngoing == True:
            for member in Roulette.party:
                actions = Actions()
                actions.user = member
                await asyncio.sleep(1)
                message = await ctx.channel.send(f'{member.mention}, it\'s your turn.', view=actions)
                actions.message = message
                await actions.wait()
                await actions.disable()
                if actions.spinned == True:
                    HardModeR1 = random.randint(1,6)
                else: pass

                async def miss():
                    await message.reply('No bullet was fired.')
                    await asyncio.sleep(1)

                async def hit():
                    chance = await message.reply('You shot yourself. A second shot will decide your fate...')
                    await asyncio.sleep(1)
                    await chance.reply('You were merely graced by the bullet. You experience minor pain.')
                    await asyncio.sleep(1)
                    await post(ctx)
                    await asyncio.sleep(3)

                async def hitcrit():
                    chance = await message.reply('You shot yourself. A second shot will decide your fate...')
                    await asyncio.sleep(1)
                    await chance.reply('You were impacted fully by the bullet. You experience severe pain.')
                    await asyncio.sleep(1)
                    await ctx.channel.send('While agonizing, you see things no human should.')
                    await asyncio.sleep(1)
                    await post(ctx,mode='degen')
                    await asyncio.sleep(5)
                    
                if (Roulette.mode == 'hard'):
                    if HardModeR1 < 6:
                        HardModeR1+=1
                        await miss()
                        continue
                    else: pass
                    if HardModeR2 < 6:
                        await hit()
                        HardModeR2+= 1
                    else:
                        HardModeR2 = random.randint(1,6)
                        await hitcrit()
                    HardModeR1 = random.randint(1,6)                  
                else:
                    if random.randint(1,6) < 6:
                        await miss()
                        continue
                    else: pass
                    if random.randint(1,6) == 6:
                        await hitcrit()
                    else:
                        await hit()     
            else:
                roundn+=1
                await ctx.channel.send('Round over.')
                await asyncio.sleep(2)

                if not Roulette.sessionOngoing == True:
                    await ctx.channel.send('Session over.')
                    return
                else: pass
                await ctx.channel.send(f'Round {roundn}:')
        else:
            actions.disable()

    @commands.hybrid_group(fallback='create', description='[NSFW] Creates a roulette group. Add \'hard\' afterwards to activate hard mode.')
    @app_commands.describe(mode='Mode to use during the session. Defaults to \'normal\'.')
    @app_commands.choices(mode=[
        app_commands.Choice(name='normal', value='normal'),
        app_commands.Choice(name='hard', value='hard')
    ])
    async def roulette(self, ctx, mode='normal'):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif Roulette.sessionOngoing == True:
            await ctx.send('There\'s already an existing session! Please wait until it ends and try again.')
            return
        elif Roulette.partyCreation == True:
            await ctx.send('This command has already been ran! If you want to join the party, type `/roulette join`.')
            return
        else: pass
        Roulette.partyCreation = True
        Roulette.party.append(ctx.author)
        Roulette.sessionMaster = ctx.author
        Roulette.mode = mode
        await ctx.send('Party created! Type \'/roulette join\' to join!')

    @roulette.command(name='join', description='[NSFW] Joins you to a session queue.')
    async def add(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif Roulette.sessionOngoing == True:
            await ctx.send('There\'s already a roulette session ongoing! Please wait until it ends.')
            return
        elif (Roulette.partyCreation == False) and (Roulette.sessionOngoing == False):
            await ctx.send('There\'s no join queue for any party! Maybe you mean \'/roulette create\' instead?')
            return
        elif ctx.author in Roulette.party:
            await ctx.send('You cannot add yourself twice!')
            return
        else: pass
        Roulette.party.append(ctx.author)
        await ctx.send('Joined the party!')

    @roulette.command(name='leave', description='[NSFW] Leave the session party.')
    async def leave(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif ctx.author == Roulette.sessionMaster:
            await ctx.send('You are the owner of the party! Maybe you meant `/roulette cancel` or `/roulette finish`?')
            return
        else: pass
        try:
            Roulette.party.remove(ctx.author)
        except ValueError:
            await ctx.send('You couldn\'t leave the party since were not in it to begin with.')
            return
        await ctx.send('You left the party.')

    @roulette.command(name='remove', description='[NSFW] Remove someone from the session party.')
    @app_commands.describe(member='The party member to remove.')
    async def remove(self, ctx, member: discord.Member):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif ctx.author != Roulette.sessionMaster:
            await ctx.send('Only the one who created the session can use this command!')
            return
        elif member == ctx.author:
            await ctx.send('You cannot remove yourself from the party! Maybe you meant `/roulette cancel` or `/roulette finish`?')
            return
        else: pass
        Roulette.party.remove(member)
        await ctx.send(f'{member.display_name} was removed.')

    @roulette.command(name='cancel', description='[NSFW] Cancel a session in standby.')
    async def cancel(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif (Roulette.partyCreation == False) or (Roulette.sessionOngoing == True):
            await ctx.send('There is no session in standby!')
            return
        elif ctx.author != Roulette.sessionMaster:
            await ctx.send('Only the one who created the session can use this command!')
            return
        else: pass
        Roulette.party = []
        Roulette.mode = ''
        Roulette.partyCreation = False
        Roulette.sessionOngoing = False
        Roulette.sessionMaster = None
        await ctx.send('Standby session has been cancelled.')

    @roulette.command(name='start', description='[NSFW] Starts a roulette session.')
    async def start(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif not ((Roulette.sessionOngoing == False) and (Roulette.partyCreation == True)):
            await ctx.send('There\'s no roulette party to start! Create one firsthand.')
            return
        elif ctx.author != Roulette.sessionMaster:
            await ctx.send('Only the one who created the session can use this command!')
            return
        else: pass
        Roulette.partyCreation = False
        Roulette.sessionOngoing = True
        await Roulette.RouletteMain(ctx)
        
    @roulette.command(name='finish', description='[NSFW] Ends a roulette session.')
    async def finish(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif (Roulette.sessionOngoing == False) or (Roulette.partyCreation == True):
            await ctx.send('There is nothing to finish! Start a session first.')
            return
        elif ctx.author != Roulette.sessionMaster:
            await ctx.send('Only the one who created the session can use this command!')
            return
        else: pass
        await ctx.send('The session will end when the round is over.')
        Roulette.sessionOngoing = False
        Roulette.mode = ''
        Roulette.party = []
        Roulette.partyCreation = False

        Roulette.sessionMaster = None

    @roulette.command(name='info-list', description='[NSFW] Lists info about the session.')
    async def info(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        elif (Roulette.sessionOngoing == False) and (Roulette.partyCreation == False):
            await ctx.send('There is no session from which to list information.')
            return
        else: pass
        embed = discord.Embed(
            color=0x1770fe,
            title='Session Info',
        )
        embed.add_field(inline=False,name='Mode',value=f'**{Roulette.mode.capitalize()}**')
        embed.add_field(inline=False,name='Leader',value=Roulette.sessionMaster.mention)
        embed.add_field(inline=False,name='Members',value=', '.join([member.mention for member in [Roulette.party.remove(Roulette.sessionMaster)]]))
        await ctx.send(embed=embed)
    
    @roulette.command(name='help', description='[NSFW] Info about the `/roulette` command.')
    async def help(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        else: pass
        embed = discord.Embed(
            color=0x1770fe,
            title='/roulette Help',
        )
        embed.add_field(name='What is this?', inline=True, value='/roulette is a command used to play Russian roulette. This roulette consists of a certain chance of getting a porn image from e621.net, with an even lesser chance of getting degeneracy.\n\nYou create a session with `/roulette create`, and then people join with `/roulette join`. When everyone is ready, use `/roulette start` to begin the session.\n\nYou can declare a mode in `/roulette create`, that is detailed on the following section.')
        embed.add_field(name='Modes', inline=True, value='`normal`: 1/6 chance of porn, 1/36 chance of REALLY messed up porn.\n\n`hard`: It behaves like a real Russian roulette, each shot gets you closer to a bullet, each bullet gets you closer to REALLY messed up porn.')
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Faith_In_Humanity(bot))
    await bot.add_cog(Roulette(bot))