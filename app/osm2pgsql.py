import os
import subprocess


def import_osm(path_name):
    subprocess.call(
        [f"osm2pgsql {path_name} -H 0.0.0.0 -P {os.getenv('POSTGRES_PORT', 5432)} -d postgres -U postgres"], shell=True
    )


if __name__ == "__main__":
    import_osm("osm_files/example.osm")
