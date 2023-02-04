# RandomBeatmap Bot

RandomBeatmap Bot is a [discord](https://discord.com/) bot that finds a random [Osu!](https://osu.ppy.sh/home) beatmap.

## Setup

- Register an Oauth application on the osu [account settings page](https://osu.ppy.sh/home/account/edit#new-oauth-application).
- Create a [Discord bot account](https://discordpy.readthedocs.io/en/stable/discord.html).
- Set environment variables however you like.

```bash
export CLIENT_ID = registered_client_id
export CLIENT_SECRET = registered_client_secret
export TOKEN = discord_bot_token
```

## Usage
- Default command prefix: ">>"
- Commands: 
  - help: >>help
  - random: >>random {GameMode}

### Main dependencies
- [Discord.py](https://discordpy.readthedocs.io/en/stable/)
- [Pydantic](https://docs.pydantic.dev/)
- [Requests](https://requests.readthedocs.io/en/latest/)