import os
from collections import namedtuple

from qgis.core import *

OsmLayer = namedtuple("OsmLayer", ("name", "type", "geometry_column"))

OSM_PREFIX = "planet_osm_"

OSM_LAYERS = ("polygon", "roads", "line", "point")


# Importing layers works fine however external styles cannot be implemented. Either custom styles need to be created
# or this quirk needs a workaround
def import_osm_layers(uri: QgsDataSourceUri):
    for osm_layer_name in OSM_LAYERS:
        name = OSM_PREFIX + osm_layer_name
        uri.setDataSource("public", name, "way")
        qgis_layer = QgsVectorLayer(uri.uri(False), name, "postgres")

        QgsProject.instance().addMapLayer(qgis_layer)


def main():
    qgs = QgsApplication([], False)
    qgs.initQgis()

    uri = QgsDataSourceUri()

    uri.setConnection("0.0.0.0", os.getenv("POSTGRES_PORT", "5432"), "postgres", "postgres", "qgis")

    qgs.exitQgis()


if __name__ == "__main__":
    main()
