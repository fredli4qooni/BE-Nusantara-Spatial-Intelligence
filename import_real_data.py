#
# Copyright FREDLI FOURQONI
#
# THIS SOFTWARE SOURCE CODE AND ANY EXECUTABLE DERIVED THEREOF ARE PROPRIETARY
# TO FREDLI FOURQONI, AS APPLICABLE, AND SHALL NOT BE USED IN ANY WAY
# OTHER THAN BEFOREHAND AGREED ON BY FREDLI FOURQONI, NOR BE REPRODUCED
# OR DISCLOSED TO THIRD PARTIES WITHOUT PRIOR AUTHORIZATION BY
# FREDLI FOURQONI, AS APPLICABLE.
#
# Author             : Fredli Fourqoni
# Version, Date      : 1.0.0, 05 Feb 2026
# Description        : ETL Script to import GeoJSON data into PostGIS and inject simulated statistics.
#
# Changelog:
# - 0.1.0 (05 Feb 2026): Initial Release with MultiPolygon support.
#

import geopandas as gpd
from sqlalchemy import create_engine
import random
import os
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

DB_USER = ""
DB_PASS = ""  
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""

FILE_NAME = "38 Provinsi Indonesia - Kabupaten.json"

print(f" Sedang membaca file {FILE_NAME}...")

try:
    if not os.path.exists(FILE_NAME):
        raise FileNotFoundError(f"File {FILE_NAME} tidak ditemukan.")

    gdf = gpd.read_file(FILE_NAME)
    print(f"Jumlah wilayah: {len(gdf)}")

except Exception as e:
    print(f" Gagal membaca file: {e}")
    exit()

print(" Normalisasi geometri (Polygon -> MultiPolygon)...")

def promote_to_multi(geom):
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    return geom

gdf['geometry'] = gdf['geometry'].apply(promote_to_multi)

print(" Menyuntikkan data statistik simulasi...")

mcts_anc = []
mcts_imm = []
housing_comp = []
housing_prog = []
housing_target = []
water_ph = []
water_f = []

for _ in range(len(gdf)):
    mcts_anc.append(random.randint(500, 5000))
    mcts_imm.append(random.randint(40, 99))
    
    target = random.randint(2000, 10000)
    comp = random.randint(500, target - 200)
    housing_target.append(target)
    housing_comp.append(comp)
    housing_prog.append(random.randint(50, target - comp))
    
    water_ph.append(round(random.uniform(5.5, 8.5), 1))
    water_f.append(round(random.uniform(0.1, 3.0), 2))

gdf['district_name'] = gdf['WADMKK']

gdf['mcts_anc_registered'] = mcts_anc
gdf['mcts_full_immunization'] = mcts_imm
gdf['housing_completed'] = housing_comp
gdf['housing_in_progress'] = housing_prog
gdf['housing_total_target'] = housing_target
gdf['water_ph'] = water_ph
gdf['water_fluoride'] = water_f

required_columns = [
    'district_name', 'mcts_anc_registered', 'mcts_full_immunization',
    'housing_completed', 'housing_in_progress', 'housing_total_target',
    'water_ph', 'water_fluoride', 'geometry'
]
final_gdf = gdf[required_columns].copy()

final_gdf = final_gdf.rename_geometry('geom')
final_gdf.set_crs(epsg=4326, inplace=True, allow_override=True)

print(" Mengupload ke PostgreSQL...")
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    final_gdf.to_postgis("district_schemes", engine, if_exists='append', index=False, chunksize=100)
    print("SUKSES! Data Real (MultiPolygon) berhasil diupload.")
except Exception as e:
    print(f"Error Upload: {e}")