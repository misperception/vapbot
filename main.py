import os, time, discord
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv('.env')

intents = discord.Intents.all()
intents.presences = False

vap = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

cogs = ["cogs.eyebleach", "cogs.fun", "cogs.trollface"]

@vap.command(name='vapreload')
async def reload(ctx, arg):
  if str(ctx.author.id) == str(os.getenv('ID')):
    if arg in cogs: 
      await ctx.channel.send(f"🟧 Reloading {arg}...")
      try:
        vap.reload_extension(arg)
        time.sleep(1)
        await ctx.channel.send(f"🟩 {arg} reloaded!")
      except Exception as e:
        print(f"{arg} couldn't be reloaded due to " + str(e))
        await ctx.channel.send(f"🟥 {arg} couldn't be reloaded. Check the console for details.")
    else:
      await ctx.channel.send("The argument is not a valid module")
  else:
    await ctx.channel.send("Maybe this is meant for someone else...")

@vap.event
async def on_ready():
  print("Loading up VapOS 1.2.0...")
  time.sleep(1)
  print("Loading modules...")
  time.sleep(3)
  for cog in cogs:
    try:
      await vap.load_extension(cog)
      time.sleep(0.5)
      print("🟩 " + cog +" was loaded successfully!")
    except Exception as e:
      print("🟥 " + cog +" couldn't load due to " + str(e))
  time.sleep(2)
  print("Loading complete! Also did you know that in terms of ma-")

async def on_disconnect():
  print("Vaporeon has breached the jar.")
  
token = os.getenv('TOKEN')
try:
  vap.run(token)
except Exception as e:
  print(f"Instance with token {token} couldn't load because of {e}")