import os, time, discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('.env')
token = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.presences = False

vap = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

cogs = ["cogs.fun", "cogs.trollface"]

@vap.hybrid_command(name='vapreload', description='Reloads command cogs or the entire command tree.')
async def reload(ctx, arg):
  if not str(ctx.author.id) == str(os.getenv('ID')):
    await ctx.send("Maybe this is meant for someone else...")
    return
  else: pass

  if (not arg in cogs) and (not arg == 'tree'): 
    await ctx.send("The argument is not a valid module.")
    return
  else: pass

  if arg == "tree":
    try:
      await vap.tree.sync()
    except:
      await ctx.send("🟥 Command tree couldn't be reloaded!")
      return
    await ctx.send("🟩 Command tree reloaded!")
    return
  else: pass
  
  await ctx.send(f"🟧 Reloading {arg}...")
  try:
    await vap.reload_extension(arg)
    time.sleep(1)
    await ctx.send(f"🟩 {arg} reloaded!")
  except Exception as e:
    print(f"{arg} couldn't be reloaded due to " + str(e))
    await ctx.send(f"🟥 {arg} couldn't be reloaded. Check the console for details.")

@vap.event
async def on_ready():
  print("Loading up VapOS 1.2.0...")
  time.sleep(1)
  print("Loading modules...")
  time.sleep(1)
  for cog in cogs:
    try:
      await vap.load_extension(cog)
      print("🟩 " + cog +" was loaded successfully!")
    except Exception as e:
      print("🟥 " + cog +" couldn't load due to " + str(e))
    time.sleep(0.2)
  await vap.tree.sync()
  time.sleep(2)
  print("Loading complete! Also did you know that in terms of ma-")

async def on_disconnect():
  print("Vaporeon has breached the jar.")

try:
  vap.run(token)
except Exception as e:
  print(f"Instance with token {token} couldn't load because of {e}")