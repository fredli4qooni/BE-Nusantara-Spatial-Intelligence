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
# Description        : Main FastAPI Application Entry Point. Handles API endpoints for fetching GIS data.
#
# Changelog:
# - 0.1.0 (05 Feb 2026): Initial Release.
#

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
import json

from database import get_db

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API Telangana GIS Aktif!"}

@app.get("/api/districts")
def get_districts_geojson(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', COALESCE(json_agg(ST_AsGeoJSON(t.*)::json), '[]'::json)
            )
            FROM district_schemes AS t;
        """)
        
        result = db.execute(query).scalar()
        
        if result is None:
            return {"type": "FeatureCollection", "features": []}
            
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))