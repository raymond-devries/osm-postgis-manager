import subprocess


def main(path_name):
    result = subprocess.call([f"osm2pgsql {path_name} -H 0.0.0.0 -P 5433 -d postgres -U postgres"], shell=True)
    print(result)


if __name__ == '__main__':
    main("map.osm")
