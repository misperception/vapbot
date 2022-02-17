import os, requests, discord, random, time
from dotenv import load_dotenv
from discord.ext import commands

vap = commands.Bot(command_prefix='v!')

with open("copypasta.txt",'r', encoding='utf-8') as texten:
  copypasta = texten.read()
with open("copypastaes.txt",'r', encoding='utf-8') as textes:
  copypastaes = textes.read()

@vap.event
async def on_ready():
  print(copypasta)

@vap.command(name='roulette')
async def roulette(ctx):
  if ctx.channel.is_nsfw():
    shot = random.randrange(1,7)
    print(f"shot = {shot}")
    if shot < 6:
      await ctx.channel.send("You fired a blank, you are safe now.")
    elif shot == 6:
      await ctx.channel.send("You fired a shot, you lose, prepare for the second roulette.")
      time.sleep(1)
      await ctx.channel.send("Preparing second roulette...")
      time.sleep(2)
      roundtwo = random.randrange(1,7)
      print(f"roundtwo = {roundtwo}")
      if roundtwo < 6:
        await ctx.channel.send("You fired a blank, loading normal porn...")
        baseURL = "https://e621.net/posts.json?page={page}&limit=1&tags=-animated"
        endpoint = baseURL.format(page = str(random.randrange(1,201)))
        head = {'User-Agent': 'VaporeonBot 1.0.0'}
        r = requests.get(endpoint, headers=head)
        jsonpage = r.json()
        posts = jsonpage['posts']
        currentpost = posts[0]
        file = currentpost['file']
        url = file['url']
        time.sleep(2)
        await ctx.send(url)
      elif roundtwo == 6:
        await ctx.channel.send("You fired a shot, loading degeneracy... hope you still have faith in humanity after this...")
        baseURL = "https://e621.net/posts.json?page={page}&limit=1&tags={tags}&-animated"
        tag = ["watersports", "omorashi", "scat", "gore", "vore", "femboy", "anal_vore", "diaper"]
        randomn = random.randrange(1,len(tag))
        endpoint = baseURL.format(page = str(random.randrange(1,201)), tags = tag[randomn - 1])
        head = {'User-Agent': 'VaporeonBot 1.0.0'}
        r = requests.get(endpoint, headers=head)
        jsonpage = r.json()
        posts = jsonpage['posts']
        currentpost = posts[0]
        file = currentpost['file']
        url = file['url']
        time.sleep(1)
        await ctx.channel.send("Brace for impact.")
        time.sleep(2)
        await ctx.send(url)
  else:
    await ctx.channel.send("Make sure to run this command on a NSFW channel.")


@vap.command(name='vapcopy')
async def copyp(ctx):
  await ctx.channel.send(copypasta)

@vap.command(name='vapcopyes')
async def copypes(ctx):
  await ctx.channel.send(copypastaes)

@vap.command(name='vapsend')
async def vapsend(ctx, arg1: discord.Member, arg2):
  try:
    arg1
    arg1 == discord.Member
  except:
    await ctx.channel.send("The first argument is not valid. (format: v!vapsend {user mention} {number of images})")
    return
  try:
    arg2
    int(arg2)
  except:
    await ctx.channel.send("The second argument is not a valid number. (format: v!vapsend {user mention} {number of images})")
  if int(arg2) <= 0:
    await ctx.channel.send("The second argument is lower or equal to zero.")
  elif int(arg2) >> 100:
    await ctx.channel.send("The second argument is higher than 100, please choose a lower number")
  else:
    baseURL = "https://e621.net/posts.json?tags=Vaporeon+-animated&limit={number}&page={page}"
    endpoint = baseURL.format(number = arg2, page = str(random.randrange(1,201)))
    head = {'User-Agent': 'VaporeonBot 1.0.0'}
    r = requests.get(endpoint, headers=head)
    jsonpage = r.json()
    posts = jsonpage['posts']
    n = len(posts)
    for index in range(n):
      print(index)
      currentpost = posts[index]
      file = currentpost['file']
      url = file['url']
      await arg1.send(url)

@vap.command(name='vappost')
async def vappost(ctx, arg):
  try:
    arg
  except:
    await ctx.channel.send("Please use the correct format. (v!vappost {number of images})")
    return
  try:
    int(arg)
  except:
    await ctx.channel.send("Argument is not a valid number.")
    return
  if int(arg) <= 0:
    await ctx.channel.send("Argument is lower or equal to zero, please choose a positive integer.")
  elif int(arg) >> 100:
    await ctx.channel.send("The second argument is higher than 100, please choose a lower number")
  else:
    baseURL = "https://e621.net/posts.json?tags=Vaporeon+-animated&limit={number}&page={page}"
    endpoint = baseURL.format(number = arg, page = str(random.randrange(1,201)))
    head = {'User-Agent': 'VaporeonBot 1.0.0'}
    r = requests.get(endpoint, headers=head)
    jsonpage = r.json()
    posts = jsonpage['posts']
    n = len(posts)
    for index in range(n):
      print(index)
      currentpost = posts[index]
      file = currentpost['file']
      url = file['url']
      await ctx.channel.send(url)


load_dotenv('.env')
vap.run(os.getenv('TOKEN'))