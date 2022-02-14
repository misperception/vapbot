import os
from discord.ext import commands
vap = commands.Bot(command_prefix='v!')
with open("copypasta.txt") as text:
  copypasta = text.read()
with open("copypastaes.txt") as textes:
  copypastaes = textes.read()

@vap.event
async def on_ready():
    print(copypasta)

@vap.command(name='copypasta')
async def copy(ctx):
    await ctx.channel.send(copypasta)

@vap.command(name='copypastaes')
async def copyes(ctx):
    await ctx.channel.send(copypastaes)



token = os.environ['TOKEN']
vap.run(token)