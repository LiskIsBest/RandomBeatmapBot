import requests

BASE_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

class OsuApi:
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
    }
    
    def __init__ (self, client_id:int=None, client_secret:str=None)->None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_type, self.__expires_in, self.access_token = self.__get_auth()
        self.authorization = self.token_type+" "+self.access_token

    def __get_auth(self):
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
        }
        body_params = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "client_credentials",
            "scope" : "public",
        }

        response = requests.post(url=TOKEN_URL, json=body_params, headers=self.headers).json()
        return response["token_type"], response["expires_in"], response["access_token"]

    def lookup_beatmap(self, beatmap_id:int|str=None, checksum:str="", filename:str="") -> dict:
        if type(beatmap_id) == int:
            beatmap_id = str(beatmap_id)
        headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization" : self.authorization
        }
        body_params = {
            "checksum" : checksum,
            "filename" : filename,
            "id" : beatmap_id,
        }

        response = requests.get(url=BASE_URL+"/beatmaps/lookup", json=body_params, headers=headers)
        
        return response.json()

