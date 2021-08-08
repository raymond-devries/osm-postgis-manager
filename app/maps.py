from qgis.core import *


def main():
    qgs = QgsApplication([], False)
    qgs.initQgis()

    uri = QgsDataSourceUri()

    uri.setConnection("0.0.0.0", "5433", "postgres", "postgres", "qgis")

    qgs.exitQgis()


if __name__ == '__main__':
    main()