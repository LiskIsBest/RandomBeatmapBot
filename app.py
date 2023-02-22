import os
from typing import Any
from random import randint
from datetime import datetime, timedelta
from dotenv import load_dotenv
import discord
from discord.ext import commands
from losuapi import AsyncOsuApi
from losuapi.types import Beatmap, GameMode
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=">>", intents=intents)
bot.remove_command("help")

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN = os.environ.get("TOKEN")
ID_MAX = 4_100_000

VALID_MODES = GameMode.list()

@bot.before_invoke
async def common(ctx: commands.Context):
	"""Runs whenever a bot command is called."""
	author = ctx.message.author
	print(f"COMMAND:{ctx.invoked_with}, USER:{author.name}, ID:{author.id}, TIME:{datetime.now().replace(microsecond=0)}")

def help_embed(ctx: commands.Context):
	"""
	Returns a Discord embed message object.

	Creates a discord.py embeded message object that shows information about the bot.

	parameters (unused):
		ctx: discord.ext.commands.Context - discord message context.
	rtype: discord.Embed
	"""
	embed = discord.Embed(title="Help", color=0xff00d0)
	embed.add_field(name="", value="**Command prefix:** `>>`", inline=False)
	embed.add_field(name="", value="**Command:** `help` - Replies with help information.", inline=False)
	embed.add_field(name="", value="**Command:** `random {Gamemode}` - Replies with a random beatmap of given map.", inline=False)
	embed.add_field(name="",value="**Valid Gamemode(s):** `osu, mania, taiko, fruits`", inline=False)
	return embed

@bot.command()
async def help(ctx: commands.Context):
	"""Discord command: >>help
	
	Sends a discord embeded message back in the same channel that the command was called.
	"""
	embed = help_embed(ctx=ctx)
	await ctx.send(embed=embed)

async def find_beatmap(api: AsyncOsuApi, arg: str|None ,wrong: list[int]) -> Beatmap | None:
	"""
	Finds a random Osu beatmap.

	Finds a random Osu beatmap, if the beatmap doesnt match the type specified in param<arg> then generate \
	a new random integer a look for a new beatmap, return the beatmap once found.

	parameters:
		api: losuapi.AsyncOsuApi - osu api client.
		arg: str|None - gamemode type string or None.
		wrong: list[int] - count of how many times the correct beatmap was not found.
	rtype: losuapi.types.Beatmap
	"""
	beatmap_id = randint(1,ID_MAX)
	beatmap = await api.lookup_beatmap(beatmap_id=beatmap_id)
	if beatmap:
		if arg:
			if beatmap.mode != arg:
				wrong[0] += 1
				beatmap = None
	return beatmap

def random_embed(ctx: commands.Context, beatmap: Beatmap)->discord.Embed:
	"""
	Returns a Discord embed message object.

	Creates a discord.py embeded message object that shows a download link, time(lenght), bpm, and gamemode(mode) of a given beatmap.

	parameters:
		ctx: discord.ext.commands.Context - context argument created of a bot command.
		beatmap: losuapi.types.Beatmap - beatmap object.
	rtype: discord.Embed
	"""
	beatmap_length = timedelta(seconds=beatmap.total_length)
	beatmap_length = ':'.join(str(beatmap_length).split(':')[1:])

	embed=discord.Embed(title=beatmap.url,description=f"Requested by {ctx.author.name}", url=beatmap.url,color=0xff00d0)
	embed.set_author(
		name=beatmap.beatmapset.artist+" - "+beatmap.beatmapset.title, 
		url=beatmap.url)
	embed.add_field(name="", value=f"**Length:** {beatmap_length} **bpm:** {int(beatmap.bpm)} **Mode:** {beatmap.mode}", inline=True)
	embed.set_image(url=beatmap.beatmapset.covers.card2x)
	return embed

@bot.command()
async def random(ctx: commands.Context, arg=None):
	"""Discord command: >>random {gamemode}
	
	Sends a discord embeded message back in the same channel that the command was called.

	parameters:
		ctx: discord.ext.commands.Context - discord message context.
		arg: Any - first text after the command call seperated by whitespace.
	"""

	if isinstance(arg, str):
		arg = arg.lower()
	if arg not in VALID_MODES:
		arg = None	
	print(f"USER:{ctx.author.name}, ARG:{arg}, TIME:{datetime.now().replace(microsecond=0)}")
	
	api = AsyncOsuApi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
	wrong_type_count = [0]
	
	beatmap = await find_beatmap(api=api, arg=arg, wrong=wrong_type_count)
	while beatmap == None:
			beatmap = await find_beatmap(api=api, arg=arg, wrong=wrong_type_count)
			
	print(f"FOUND:{beatmap.url}, MODE:{beatmap.mode}, STATUS:{(beatmap.status).lower()}, TRIES:{wrong_type_count[0]}")

	embed = random_embed(ctx=ctx, beatmap=beatmap)
	await ctx.send(embed=embed)

bot.run(TOKEN)