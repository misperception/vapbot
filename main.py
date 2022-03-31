import os, requests, discord, random, time
from dotenv import load_dotenv
from discord.ext import commands

vap = commands.Bot(command_prefix='v!')

cogs = ["cogs.eyebleach", "cogs.fun", "cogs.trollface"]

@vap.event
async def on_ready():
  print("Loading up VapOS 1.2.0...")
  time.sleep(1)
  print("Loading modules...")
  time.sleep(3)
  for cog in cogs:
    try:
      vap.load_extension(cog)
      time.sleep(0.5)
      print("🟩 " + cog +" was loaded successfully!")
    except Exception as e:
      print("🟥 " + cog +" couldn't load due to " + str(e))
  time.sleep(2)
  print("Loading complete! Also did you know that in terms of ma-")

load_dotenv('.env')
vap.run(os.getenv('TOKEN'))