import random
import geopandas as gpd
from sqlalchemy import create_engine
import json

DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""

print("1. Menyiapkan data dummy...")
districts = [
    {"name": "District A", "coords": [[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]},
    {"name": "District B", "coords": [[10, 0], [10, 10], [20, 10], [20, 0], [10, 0]]},
    {"name": "District C", "coords": [[0, 10], [0, 20], [10, 20], [10, 10], [0, 10]]},
    {"name": "District D", "coords": [[10, 10], [10, 20], [20, 20], [20, 10], [10, 10]]},
]

features = []
for d in districts:
    properties = {
        "district_name": d["name"],
        "mcts_anc_registered": random.randint(60, 100),
        "mcts_full_immunization": random.randint(50, 95),
        "housing_completed": random.randint(1000, 4000),
        "housing_in_progress": random.randint(500, 1000),
        "housing_total_target": 5000,
        "water_ph": round(random.uniform(5.5, 9.0), 1),
        "water_fluoride": round(random.uniform(0.5, 2.5), 2),
    }
    features.append({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [d["coords"]]},
        "properties": properties
    })

geojson_obj = {"type": "FeatureCollection", "features": features}

print("2. Mengupload ke database...")
connection_str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_str)

try:
    gdf = gpd.GeoDataFrame.from_features(geojson_obj["features"])
    
    gdf.set_crs(epsg=4326, inplace=True)

    gdf = gdf.rename_geometry('geom') 
    
    gdf.to_postgis("district_schemes", engine, if_exists='append', index=False)
    print("SUKSES! Data berhasil dimasukkan.")
except Exception as e:
    print(f"ERROR: {e}")