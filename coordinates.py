import requests, mercantile
import geojson
import os
from dotenv import load_dotenv

load_dotenv()
metadata_endpoint = "https://graph.mapillary.com"

# east, south, west, north = [120.983336, 14.438567, 120.983336, 14.438567]
east, south, west, north = [120.98384, 14.53304, 120.99384, 14.54304]

tiles = list(mercantile.tiles(east, south, west, north, 18))
bbox_list = [mercantile.bounds(tile.x, tile.y, tile.z) for tile in tiles]
client_token = os.getenv("ACCESS_TOKEN")

features = []

path = "data/mapillary/paranaque"


bbox_features = []
bbox_str = str(f'{west},{south},{east},{north}')
url = f"https://graph.mapillary.com/images?access_token={client_token}&fields=id,geometry,is_pano,thumb_2048_url&bbox={bbox_str}&is_pano=false"
response = requests.get(url)
print(response)
if response.status_code == 200:
    json = response.json()
    print(json)
