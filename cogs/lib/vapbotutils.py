import discord

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