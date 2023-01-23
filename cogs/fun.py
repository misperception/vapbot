import random, requests, discord, asyncio
import pandas as pd
from discord.ext import commands
from discord import app_commands
with open("copypasta.txt",'r', encoding='utf-8') as texten:
  copypasta = texten.read()
with open("copypastaes.txt",'r', encoding='utf-8') as textes:
  copypastaes = textes.read()
head = {'User-Agent': 'VapBot 1.2.0'}

class ParseUtils:
    dict_rating = {
            's': 'safe',
            'q': 'questionable',
            'e': 'explicit'
        }
    dict_color = {
            's': 0x56ff30,
            'q': 0xffb730,
            'e': 0xff3030
        }

    async def EmbedMaker(post, ctx):
        rating = post.get('post').get('rating')
        url = post.get('post').get('file').get('url')
        tags = post.get('post').get('tags').get('general')
        usetags = 'Tags: ' + ', '.join(tags)
        
        imageembed = discord.Embed(color=ParseUtils.dict_color[rating], title=ParseUtils.dict_rating.get(rating).capitalize())
        imageembed.set_image(url=url)
        imageembed.set_footer(text=usetags, icon_url='https://e621.net/favicon.ico')
        await ctx.send(embed=imageembed)

class Fun(commands.Cog):
    def __init__(bot, self):
        self.bot = bot

    @commands.hybrid_command(name='roulette', description='[NSFW] 1/6th chance of getting porn, 1/36th chance of getting REALLY messed up porn.')
    async def roulette(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send("Make sure to run this command on a NSFW channel.")
            return
        else: pass

        author = ctx.author.mention
        shot = random.randrange(1,7)

        if shot < 6:
            await ctx.send(f"{author}, you fired a blank, you are safe now.")
            return
        elif shot == 6: pass

        await ctx.send(f"{author}, you fired a shot, you lose, prepare for the second roulette.")
        await asyncio.sleep(1)
        await ctx.send("Preparing second roulette...")
        await asyncio.sleep(2)
        roundtwo = random.randrange(1,7)

        if not roundtwo == 6:
            await ctx.send(f"{author}, you fired a blank, loading normal porn...")
            endpoint = "https://e621.net/posts/random.json?tags=-animated+rating:explicit+-vore+-anal_vore+-urine+-feces+-diaper"
            r = requests.get(endpoint, headers=head)
            jsonpage = r.json()
            await asyncio.sleep(2)
            try:
                await ParseUtils.EmbedMaker(jsonpage,ctx)
            except:
                await ctx.send('The bullet got stuck! Lucky!')
            return

        else:
            await ctx.send(f"{author}, you fired a shot, loading degeneracy... hope you still have faith in humanity after this...")
            baseURL = "https://e621.net/posts/random.json?tags={tags}+-animated"
            tag = ["watersports", "omorashi", "scat", "gore", "vore", "anal_prolapse", "anal_vore", "diaper", "intersex+breasts", "ear_penetration", "fart"]
            randomn = random.randrange(1,len(tag))
            endpoint = baseURL.format(tags = tag[randomn - 1])
            r = requests.get(endpoint, headers=head)
            jsonpage = r.json()
            await asyncio.sleep(1)
            await ctx.send("Brace for impact.")
            await asyncio.sleep(2)
            try:
                await ParseUtils.EmbedMaker(jsonpage,ctx)
            except:
                await ctx.send("Crisis averted. You'd better be grateful.")

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
        currentpost = requests.get(endpoint, headers=head).json()
        await ParseUtils.EmbedMaker(currentpost, ctx)
class Faith_In_Humanity(commands.Cog, name='Faith in humanity'):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='eyebleach', description='Restores a small part of your faith in humanity.')
    async def eyebleach(self, ctx):
        endpoint = "https://e621.net/posts/random.json?tags=vaporeon+rating:safe+-breasts"
        head = {'User-Agent': 'VaporeonBot 1.0.0'}
        r = requests.get(endpoint, headers=head).json()
        try:
            await ParseUtils.EmbedMaker(r,ctx)
        except:
            await ctx.send("For whatever reason, *ahem, ahem, check the console* the image couldn't be sent. Sucks to be you, huh?")

async def setup(bot):
    await bot.add_cog(Fun(bot))
    await bot.add_cog(Faith_In_Humanity(bot))