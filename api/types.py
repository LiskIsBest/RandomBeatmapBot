from enum import Enum
# import datetime
from pydantic import BaseModel, Field

class GameMode(Enum):
    OSU = "osu"
    MANIA = "mania"
    FRUITS = "fruits"
    TAIKO = "taiko"

class Covers(BaseModel):
    cover: str
    cover2x: str = Field(alias="cover@2x")
    card: str
    card2x: str = Field(alias="card@2x")
    cover_list: str = Field(alias="list")
    cover_list2x: str = Field(alias="list@2x")
    slimcover: str
    slimcover: str = Field(alias="slimcover@2x")
    
    
class BeatmapsetCompact(BaseModel):
    artist: str
    artist_unicode: str
    covers

