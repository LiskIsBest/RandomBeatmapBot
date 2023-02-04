import os
import json
from dotenv import load_dotenv
from api import OsuApi
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

api = OsuApi(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# TEST_ID = 1215686
TEST_ID = 2562376

with open("dump2.json", "w") as f:
    f.write(json.dumps(obj=api.lookup_beatmap(TEST_ID), indent=4, separators=(",", ":")))