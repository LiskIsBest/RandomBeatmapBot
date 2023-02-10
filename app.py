import os
from random import randint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import discord
from discord.ext import commands
from losuapi import AsyncOsuApi
from losuapi.types import Beatmap
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">>", intents=intents)
bot.remove_command("help")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")
ID_MAX = 4_100_000

VALID_MODES = {"osu","mania","fruits","taiko"}

def random_embed(beatmap: Beatmap, ctx: commands.Context)->discord.Embed:
	beatmap_length = timedelta(seconds=beatmap.total_length)
	beatmap_length = ':'.join(str(beatmap_length).split(':')[1:])

	embed=discord.Embed(title=beatmap.url,description=f"Requested by {ctx.author.name}", url=beatmap.url,color=0xff00d0)
	embed.set_author(
		name=beatmap.beatmapset.artist+" - "+beatmap.beatmapset.title, 
		url=beatmap.url)
	embed.add_field(name="", value=f"**Length:** {beatmap_length} **bpm:** {int(beatmap.bpm)} **Mode:** {beatmap.mode}", inline=True)
	embed.set_image(url=beatmap.beatmapset.covers.card2x)
	return embed

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
		print("Arg is None")
		arg = None
	else:
		print(f"Arg is: {arg}")
	
	api = AsyncOsuApi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	print(f"{ctx.author.name}:API_CONNECTED")

	beatmap_id = randint(1,ID_MAX)
	try:
		beatmap = await api.lookup_beatmap(beatmap_id=beatmap_id)
		if arg:
			if beatmap.mode != arg:
				print(f"{ctx.author.name}:WRONG_TYPE_{beatmap.mode.upper()}")
				beatmap = None
		else:
			...
	except:
		beatmap = None
	while beatmap == None:

			beatmap_id = randint(1,ID_MAX)
			try:
				beatmap = await api.lookup_beatmap(beatmap_id=beatmap_id)
				if arg:
					if beatmap.mode != arg:
						print(f"{ctx.author.name}:WRONG_TYPE_{beatmap.mode.upper()}")
						beatmap = None
				else:
					...
			except:
				beatmap = None
	print(f"FOUND:{beatmap.url}, MODE:{beatmap.mode}, STATUS:{(beatmap.status).lower()}")

	embed = random_embed(beatmap, ctx=ctx)
	await ctx.send(embed=embed)
	
try:
	bot.run(TOKEN)
except:
	print("Failed")
