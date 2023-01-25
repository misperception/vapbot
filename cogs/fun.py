import random, requests, asyncio, discord
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

    async def RouletteMain(ctx):
        roundn = 1

        class Actions(discord.ui.View):
            shot = False
            spinned = False
            @discord.ui.button(label='Shoot!',style=discord.ButtonStyle.danger)
            async def shoot(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.shot = True
                interaction.response.send_message('*click*',ephemeral=True,delete_after=0.3)
                self.stop()
            
            if Roulette.mode == 'hard':
                @discord.ui.button(label='Spin',style=discord.ButtonStyle.primary)
                async def spin(self, interaction: discord.Interaction, button: discord.ui.Button):
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

            await ParseUtils.EmbedMaker(endpoint.get(mode),ctx)

        HardModeR1 = random.randint(1,6)
        HardModeR2 = random.randint(1,6)
        while Roulette.sessionOngoing == True:
            for member in Roulette.party:
                actions = Actions()
                await asyncio.sleep(1)
                message = await ctx.send(f'{member.mention}, it\'s your turn.', view=actions)
                actions.message = message
                await actions.wait()
                await actions.disable()
                if actions.spinned == True:
                    HardModeR1 = random.randint(1,6)
                else:pass

                if (Roulette.mode == 'hard'):

                    if HardModeR1 == 6:
                        await ctx.send('You shot yourself. A second shot will decide your fate.')
                        await asyncio.sleep(1)
                        
                        if HardModeR2 < 6:
                            await ctx.send('You were merely graced by the bullet. You experience minor pain.')
                            HardModeR2+= 1
                            await asyncio.sleep(1)
                            await post(ctx)
                            await asyncio.sleep(3)
                        else:
                            await ctx.send('You were impacted fully by the bullet. You experience severe pain.')
                            HardModeR2 = random.randint(1,6)
                            await asyncio.sleep(1)
                            await ctx.send('While agonizing, you see things no human should.')
                            await post(ctx,mode='degen')
                            await asyncio.sleep(5)

                        HardModeR1 = random.randint(1,6)
                    else:
                        await ctx.send('No bullet was fired.')
                        HardModeR1+=1
                else:
                    if random.randint(1,6) == 6: #first shot
                        await ctx.send('You shot yourself. A second shot will decide your fate') 
                        asyncio.sleep(1)
                        if random.randint(1,6) == 6: #second shot
                            await ctx.send('You were impacted fully by the bullet. You experience severe pain.')
                            await asyncio.sleep(1)
                            await ctx.send('While agonizing, you see things no human should.')
                            await post(ctx, mode='degen')
                            await asyncio.sleep(5)
                        else:
                            await ctx.send('You were merely graced by the bullet. You experience minor pain.')
                            await asyncio.sleep(1)
                            await post(ctx)
                            await asyncio.sleep(3)
                    else:
                        await ctx.send('No bullet was fired.')
            else:
                roundn+=1
                await ctx.send('Round over.')
                await asyncio.sleep(2)
                await ctx.send(f'Round {roundn}:')
        else: Actions.disable()

    @commands.hybrid_group(fallback='create', description='Creates a roulette group. Add \'hard\' afterwards to activate hard mode.')
    @app_commands.describe(mode='Mode to use during the session. Defaults to \'normal\'.')
    @app_commands.choices(mode=[
        app_commands.Choice(name='normal', value='normal'),
        app_commands.Choice(name='hard', value='hard')
    ])
    async def roulette(self, ctx, mode='normal'):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        else: pass
        if Roulette.sessionOngoing == True:
            await ctx.send('There\'s already an existing session! Please wait until it ends and try again.')
            return
        elif Roulette.partyCreation == True:
            await ctx.send('This command has already been ran! If you want to join the party, type \'/roulette join\'.')
            return
        else: pass
        Roulette.partyCreation = True
        Roulette.party.append(ctx.author)
        Roulette.mode = mode
        await ctx.send('Party created! Type \'/roulette join\' to join!')

    @roulette.command(name='join', description='Joins you to a session queue.')
    async def add(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        else: pass
        if Roulette.sessionOngoing == True:
            await ctx.send('There\'s already a roulette session ongoing! Please wait until it ends.')
            return
        elif (Roulette.partyCreation == False) and (Roulette.sessionOngoing == False):
            await ctx.send('There\'s no join queue for any party! Maybe you mean \'/roulette create\' instead?')
            return
        else: pass
        Roulette.party.append(ctx.author)
        await ctx.send('Joined the party!')

    @roulette.command(name='start', description='Starts a roulette session.')
    async def start(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        else: pass
        if not ((Roulette.sessionOngoing == False) and (Roulette.partyCreation == True)):
            await ctx.send('There\'s no roulette party to start! Create one firsthand.')
            return
        else: pass
        Roulette.partyCreation = False
        Roulette.sessionOngoing = True
        await Roulette.RouletteMain(ctx)
        
    @roulette.command(name='finish', description='Ends a roulette session.')
    async def finish(self,ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send('Make sure to run this in a NSFW channel')
            return
        else: pass
        if Roulette.sessionOngoing == False:
            await ctx.send('There is nothing to finish! Run a session first.')
            return
        else: pass
        await ctx.send('Session finished!')
        Roulette.sessionOngoing = False

async def setup(bot):
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Faith_In_Humanity(bot))
    await bot.add_cog(Roulette(bot))