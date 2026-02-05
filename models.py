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
# Description        : SQLAlchemy Models definition for District Schemes table.
#
# Changelog:
# - 0.1.0 (05 Feb 2026): Initial Release.
#

from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from database import Base

class DistrictScheme(Base):
    __tablename__ = "district_schemes"

    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String)
    
    mcts_anc_registered = Column(Integer)
    mcts_full_immunization = Column(Integer)
    
    housing_completed = Column(Integer)
    housing_in_progress = Column(Integer)
    housing_total_target = Column(Integer)
    
    water_ph = Column(Float)
    water_fluoride = Column(Float)
    
    geom = Column(Geometry('POLYGON', srid=4326))