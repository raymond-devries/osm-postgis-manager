import os
import subprocess

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)


def execute_query(query: str, db_name: str = "postgres"):
    conn = psycopg2.connect(dbname=db_name, user="postgres", password="qgis", port=POSTGRES_PORT, host="0.0.0.0")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def create_db(db_name: str):
    execute_query(f"CREATE DATABASE {db_name};")
    execute_query("CREATE EXTENSION postgis", db_name)


def drop_db(db_name: str):
    execute_query(f"DROP DATABASE {db_name}")


def import_osm(path_name: str, db_name: str):
    create_db(db_name)
    subprocess.call([f"osm2pgsql {path_name} -H 0.0.0.0 -P {POSTGRES_PORT} -d {db_name} -U postgres"], shell=True)
    execute_query(
        "ALTER TABLE planet_osm_point ADD gid serial PRIMARY KEY;"
        "ALTER TABLE planet_osm_line ADD gid serial PRIMARY KEY;"
        "ALTER TABLE planet_osm_polygon ADD gid serial PRIMARY KEY;"
        "ALTER TABLE planet_osm_roads ADD gid serial PRIMARY KEY;",
        db_name,
    )
