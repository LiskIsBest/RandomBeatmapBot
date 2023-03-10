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
- Commands: 
  - help: /help
  - random: /random {GameMode}

![](https://media.giphy.com/media/I6TUJS7yNhRXiw9U5a/giphy.gif)

### Main dependencies
- [Losuapi](https://github.com/LiskIsBest/Losuapi)
- [Pycord](https://docs.pycord.dev/en/stable/)
- [Pydantic](https://docs.pydantic.dev/)
