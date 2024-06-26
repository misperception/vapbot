import os, time, discord
from discord.ext import commands


TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
ID = os.getenv('ID')

intents = discord.Intents.all()
intents.presences = False

vap = commands.Bot(command_prefix=PREFIX, intents=intents)

cogs = ["cogs.fun", "cogs.trollface", "cogs.music"]

@vap.hybrid_command(name='vapreload', description='Reloads command cogs or the entire command tree.')
async def reload(ctx, arg):
  if str(ctx.author.id) != str(ID):
    await ctx.send("Maybe this is meant for someone else...")
    return
  elif (not arg in cogs) and (not arg == 'tree'): 
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
  await ctx.send(f"🟧 Reloading {arg}...")
  try:
    await vap.reload_extension(arg)
    await vap.tree.sync()
    time.sleep(1)
    await ctx.send(f"🟩 {arg} reloaded!")
  except Exception as e:
    print(f"{arg} couldn't be reloaded due to " + str(e))
    await ctx.send(f"🟥 {arg} couldn't be reloaded. Check the console for details.")

@vap.event
async def on_ready():
  print("Loading up VapOS 1.3.0...")
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
  print("🟦 Loading command tree...")
  try:
    await vap.tree.sync()
    print("🟩 Command tree finished loading!")
  except TimeoutError:
    print("🟥 Command tree took too long to load!")
  time.sleep(2)
  print("Loading complete! Also did you know that in terms of ma-")
@vap.event
async def on_disconnect():
  print("Vaporeon has breached the jar.")

try:
  vap.run(TOKEN)
except Exception as e:
  print(f"Instance with token {TOKEN} couldn't load because of {e}")
