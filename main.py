import os, requests
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

@vap.command(name='vappost')
async def vappost(ctx, arg):
  try:
    int(arg)
  except:
    await ctx.channel.send("Argument is not a valid number")
  if int(arg) <= 0:
    await ctx.channel.send("Argument is lower or equal to zero, please choose a positive integer")
  else:
    baseURL = "https://e621.net/posts.json?tags=Vaporeon+-animated&limit="
    endpoint = f"{baseURL}{arg}"
    r = requests.get(endpoint)
    json = r.json()

token = os.environ['TOKEN']
vap.run(token)