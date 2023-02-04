import os
from random import randint
from asyncio import sleep as asyncsleep
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands
from ossapi import Ossapi
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">>", intents=intents)
bot.remove_command("help")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")
ID_MAX = 5_000_000

VALID_MODES = ("osu","mania","fruits","taiko")

@bot.before_invoke
async def common(ctx: commands.Context):
	author = ctx.message.author
	print(f"USER:{author.name}, ID:{author.id}, COMMAND:{ctx.invoked_with}, TIME:{datetime.now().replace(microsecond=0)}")

@bot.command()
async def help(ctx: commands.Context):
	await ctx.send('Commands:\n  >>givemap [osu, mania, taiko, fruits]\n  fruits = Catch the beat')

@bot.command()
async def random(ctx: commands.Context, arg=""):
	
	if arg not in VALID_MODES:
		print("Setting arg to None")
		arg = None
	else:
		print(f"Arg is: {arg}")
	
	api = Ossapi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

	await asyncsleep(0)
	print(f"{ctx.author.name}:API_CONNECTED")

	beatmap_id = randint(1,ID_MAX)
	try:
		beatmap = api.beatmap(beatmap_id=beatmap_id)
	except:
		beatmap = None
	while beatmap == None:
			# await ctx.send(f"{ctx.author.name}:BEATMAP_NONE")
			await asyncsleep(0)
			print(f"{ctx.author.name}:BEATMAP_NONE")

			beatmap_id = randint(1,ID_MAX)
			try:
				beatmap = api.beatmap(beatmap_id=beatmap_id)
				if arg == None:
					...
				elif beatmap.mode.value != arg:
					beatmap = None
			except:
				beatmap = None
	print(f"FOUND:{beatmap.url}, MODE:{beatmap.mode.value}, STATUS:{(beatmap.status.name).lower()}")
	await ctx.send(f"{ctx.message.author.name} requested a random{' '+arg if arg != None else ''} beatmap: {beatmap.url}")
	
try:
	bot.run(TOKEN)
except:
	print("Failed")
