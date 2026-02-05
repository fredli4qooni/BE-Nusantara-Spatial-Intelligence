# Nusantara Spatial Intelligence (NSI) - Backend Architecture

## Abstract

The Backend component of the Nusantara Spatial Intelligence (NSI) system serves as the core computational and data retrieval unit. Built upon the FastAPI framework, this service implements a high-performance RESTful API designed to query, transform, and serve geospatial data stored in a PostgreSQL database extended with PostGIS. The system is engineered to handle complex spatial geometries (MultiPolygons) and attribute data simultaneously, ensuring efficient data delivery to the visualization layer.

## Technology Stack

The server-side infrastructure utilizes the following technologies:

* **Language:** Python 3.10+
* **Framework:** FastAPI (Asynchronous Web Framework)
* **Database:** PostgreSQL 14+ with PostGIS Extension
* **ORM:** SQLAlchemy with GeoAlchemy2 for spatial data handling
* **Data Processing:** GeoPandas and Shapely for geometry manipulation

## Prerequisites

Before initiating the installation process, ensure the following software is installed and configured in the environment:

1. Python 3.10 or higher.
2. PostgreSQL Database Server.
3. PostGIS Extension for PostgreSQL.
4. pip (Python Package Installer).

## Installation and Configuration

### 1. Environment Setup

It is recommended to use a virtual environment to isolate dependencies.
```bash
python -m venv venv
# Windows activation
.\venv\Scripts\activate
# Linux/macOS activation
source venv/bin/activate
```

### 2. Dependency Installation

Install the required Python libraries as specified in the requirements.
```bash
pip install fastapi uvicorn sqlalchemy geoalchemy2 psycopg2-binary geopandas shapely
```

### 3. Database Configuration

Create a PostgreSQL database and enable the PostGIS extension. Ensure the credentials match the configuration in `database.py` and `import_real_data.py`.
```sql
CREATE DATABASE nsi_db;
\c nsi_db
CREATE EXTENSION postgis;
```

### 4. Data Migration and ETL

Execute the ETL (Extract, Transform, Load) script to ingest the GeoJSON raw data, normalize geometry types to MultiPolygon, and inject simulation statistics into the database schema.
```bash
python import_real_data.py
```

*Note: Ensure the source file "38 Provinsi Indonesia - Kabupaten.json" is present in the root directory before execution.*

## Execution

To run the server in a development environment, execute the Uvicorn server:
```bash
uvicorn main:app --reload
```

The API will operate on `http://127.0.0.1:8000`.

## API Endpoints specification

* **GET /**: Health check endpoint. Returns the operational status of the API.
* **GET /api/districts**: Retrieves the complete spatial dataset in GeoJSON format, including attribute data for Water Quality, Housing, and Health metrics.

## Copyright and License

Copyright FREDLI FOURQONI

THIS SOFTWARE SOURCE CODE AND ANY EXECUTABLE DERIVED THEREOF ARE PROPRIETARY TO FREDLI FOURQONI, AS APPLICABLE, AND SHALL NOT BE USED IN ANY WAY OTHER THAN BEFOREHAND AGREED ON BY FREDLI FOURQONI, NOR BE REPRODUCED OR DISCLOSED TO THIRD PARTIES WITHOUT PRIOR AUTHORIZATION BY FREDLI FOURQONI, AS APPLICABLE.

Author: Fredli Fourqoni