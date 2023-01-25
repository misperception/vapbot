import discord, requests

class ParseUtils:
    dict_rating = {
            's': 'safe',
            'q': 'questionable',
            'e': 'explicit'
        }
    dict_color = {
            's': 0x56ff30,
            'q': 0xffb730,
            'e': 0xff3030,
            '?': 0x555555
        }

    async def EmbedMaker(endpoint, ctx):
        head = {'User-Agent': 'VapBot 1.2.0'}
        post = requests.get(endpoint, headers=head).json()
        try:
            rating = post.get('post').get('rating')
        except: rating = '?'
        url = post.get('post').get('file').get('url')
        tags = post.get('post').get('tags').get('general')
        usetags = 'Tags: ' + ', '.join(tags)
        
        imageembed = discord.Embed(color=ParseUtils.dict_color[rating], title=ParseUtils.dict_rating.get(rating).capitalize())
        imageembed.set_image(url=url)
        imageembed.set_footer(text=usetags, icon_url='https://e621.net/favicon.ico')
        await ctx.send(embed=imageembed)