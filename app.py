import os
from random import randint
from asyncio import sleep as asyncsleep
from datetime import datetime, timedelta
from dotenv import load_dotenv
import discord
from discord.ext import commands
from api import OsuApi
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">>", intents=intents)
bot.remove_command("help")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")
ID_MAX = 4_100_000

VALID_MODES = ("osu","mania","fruits","taiko")

@bot.before_invoke
async def common(ctx: commands.Context):
	author = ctx.message.author
	print(f"USER:{author.name}, ID:{author.id}, COMMAND:{ctx.invoked_with}, TIME:{datetime.now().replace(microsecond=0)}")

@bot.command()
async def help(ctx: commands.Context):
	await ctx.send('Commands:\n  >>givemap [osu, mania, taiko, fruits]\n  fruits = Catch the beat')

@bot.command()
async def random(ctx: commands.Context, arg=None):
	
	if arg not in VALID_MODES:
		print("Setting arg to None")
		arg = None
	else:
		print(f"Arg is: {arg}")
	
	api = OsuApi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

	await asyncsleep(0)
	print(f"{ctx.author.name}:API_CONNECTED")

	beatmap_id = randint(1,ID_MAX)
	try:
		beatmap = api.lookup_beatmap(beatmap_id=beatmap_id)
	except:
		beatmap = None
	while beatmap == None:
			await asyncsleep(0)

			beatmap_id = randint(1,ID_MAX)
			try:
				beatmap = api.lookup_beatmap(beatmap_id=beatmap_id)
				if arg == None:
					...
				elif (mode := beatmap.mode.value) != arg:
					print(f"{ctx.author.name}:BEATMAP_{mode.upper()}")
					beatmap = None
			except:
				beatmap = None
	print(f"FOUND:{beatmap.url}, MODE:{beatmap.mode.value}, STATUS:{(beatmap.status).lower()}")

	beatmap_length = timedelta(seconds=beatmap.total_length)
	beatmap_length = ':'.join(str(beatmap_length).split(':')[1:])

	embed=discord.Embed(title=beatmap.url,description=f"Requested by {ctx.author.name}", url=beatmap.url,color=0xff00d0)
	embed.set_author(
		name=beatmap.beatmapset.artist+" - "+beatmap.beatmapset.title, 
		url=beatmap.url)
	embed.add_field(name="", value=f"**Length:** {beatmap_length} **bpm:** {int(beatmap.bpm)} **Mode:** {beatmap.mode.value}", inline=True)
	embed.set_image(url=beatmap.beatmapset.covers.card2x)
	await ctx.send(embed=embed)
	
try:
	bot.run(TOKEN)
except:
	print("Failed")