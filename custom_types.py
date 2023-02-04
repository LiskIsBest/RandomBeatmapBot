from enum import Enum
import datetime

class GameMode(Enum):
    OSU = "osu"
    MANIA = "mania"
    FRUITS = "fruits"
    TAIKO = "taiko"

class BeatmapData:
    def __init__(self,
            beatmapset_id: int,
            beatmap_id: int,
            difficulty_rating: float,
            mode: str,
            status: str,
            bpm: int,
            max_combo: int,
            url: str,
            version: str,
            artist: str,
            title: str,
            length: int
            ):
        self.beatmapset_id = beatmapset_id
        self.beatmap_id = beatmap_id
        self.difficulty_ration = difficulty_rating
        self.mode = mode
        self.status = status
        self.bpm = bpm
        self.max_combo = max_combo
        self.url = url
        self.version = version
        self.title = artist+" - "+title
        self.length = length
        self.str_length = self.get_length_str()
        
    def get_length_str(self):
        return str(datetime.timedelta(seconds=self.length))