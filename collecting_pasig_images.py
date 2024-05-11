import requests, mercantile
import geojson
import os
from dotenv import load_dotenv

load_dotenv()
metadata_endpoint = "https://graph.mapillary.com"

east, south, west, north = [121.064483, 14.534038, 121.116208, 14.615116]
tiles = list(mercantile.tiles(east, south, west, north, 18))
bbox_list = [mercantile.bounds(tile.x, tile.y, tile.z) for tile in tiles]

client_token = os.getenv("ACCESS_TOKEN")

features = []

path = "data/mapillary/pasig"
try:
    os.makedirs(path)
    print("Folder %s created!" % path)
except FileExistsError:
    print("Folder %s already exists" % path)

for i, bbox in enumerate(bbox_list):
    bbox_features = []
    bbox_str = str(f'{bbox.west},{bbox.south},{bbox.east},{bbox.north}')
    url = f"https://graph.mapillary.com/images?access_token={client_token}&fields=id,geometry,is_pano,thumb_2048_url&bbox={bbox_str}&is_pano=false"
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
  
        # check if the response is empty or not
        if len(json["data"]):
            for obj in json["data"]:
  
                # build a GeoJSON object for each feature
                feature = geojson.Feature(geometry=obj["geometry"], properties={"id": obj["id"],"is_pano": obj["is_pano"], "thumb_2048_url": obj.get("thumb_2048_url", None)})

                bbox_features.append(feature)


        featureCollection = geojson.FeatureCollection(bbox_features)
        dump = geojson.dumps(featureCollection)


        with open(f"{path}/pasig{i}.geojson", "w") as outfile:
          outfile.write(dump)