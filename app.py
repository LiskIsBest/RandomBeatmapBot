import os
from random import randint
from dotenv import load_dotenv
import discord
from discord.ext import commands
from ossapi import Ossapi
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">>", intents=intents)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")
ID_MAX = 5_000_000

@bot.command()
async def givemap(ctx):
	api = Ossapi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	beatmap_id = randint(1,ID_MAX)
	
	try:
		beatmap = api.beatmap(beatmap_id=beatmap_id)
	except:
		beatmap = None
	while beatmap == None:
		beatmap_id = randint(1,ID_MAX)
		try:
			beatmap = api.beatmap(beatmap_id=beatmap_id)
		except:
			beatmap = None

	await ctx.send(f"Random beatmap: {beatmap.url}")
	
try:
	bot.run(TOKEN)
except:
	print("Failed")
