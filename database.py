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
# Description        : Database connection configuration using SQLAlchemy.
#
# Changelog:
# - 0.1.0 (05 Feb 2026): Initial Release.
#

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()