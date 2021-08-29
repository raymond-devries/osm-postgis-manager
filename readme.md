# OSM POSTGIS Manager

---

### What is this?
This tool helps manage and create POSTGIS databases based on OSM (Open Street Map) data. The tool is completely managed through an easy-to-use web interface.

### Security Warning
This tool is meant to be used exclusively on your local machine. It is not meant for web deployment.

### Requirements

The only requirements are docker and docker-compose. If on Windows or Mac I suggest you install Docker Desktop which includes docker and docker-compose and can be found [here](https://docs.docker.com/desktop/). If on linux, the appropriate engine needs to be installed. Instructions for particular distros can be found [here](https://docs.docker.com/engine/install/).
> I could not get this working on my M1 ARM mac. If you have any luck or know of a solution of how to get this working on a M1 Mac please open an issue or a pull request.

### How to use

The only file needed to run this is the docker-compose.yml file found in the repository. The file can be downloaded directly from [here](https://gist.github.com/raymond-devries/f6ca04433333648b494c1abe109f05d8/archive/9e68888834b01d66e75cb0b3cdb619f3afbe0b2d.zip). Navigate using the terminal to the directory containing the docker-compose.yml file and use the following command to start the tool:

`docker-compose up -d`

This will start the tool in the background. The first time this command is run it will take a while to download and unpack the needed resources. When the tool is started again the tool should start very quickly. Once the startup process has completed go to [http://localhost:5000/](http://localhost:5000/) in the browser. From the web interface OSM files can be uploaded and turned into POSTGIS databases for use on your local machine. This can be very useful when using OSM data in GIS software such as QGIS.

To stop the tool use the following command in the directory containing the docker-compose.yml file:

`docker-compose down`

By default, all files and databases used in the tool are saved on the local machine. When the tool is restarted the files and databases uploaded/created previously will be available for use. To remove all uploaded osm files and databases on a local machine use the following command instead when stopping the tool.

`docker-compose down -v`

### Technical Notes

This tool uses a flask app running in DEBUG mode for the front end. This allows users to more easily report bugs since this tool is intended only to be run on the local machine. The front end uses Bulma as the CSS Framework, Alpine JS for interactivity and HTMX to allow dynamic loading of HTML content. The OSM to POSTGIS conversion is performed by the very popular tool osm2pgsql. Since osm2pgsql does not include primary keys for all entries this is done when the database is created to prevent confusing errors when paths, polygons, etc. are edited in GIS software. 


### Why was this tool created?

Aside from personal convenience, this tool was created to lower the technical barriers of turing OSM files in POSTGIS databases. I have friends who enjoy mapping and need to create maps for adventure races. Installing all the needed dependencies and then having to operate them from the command line creates a technical barrier to entry for those who are not familiar with the command line, databases and quirks that come with installing things for their particular operating system. This only requires one tool to be installed on your system, Docker Desktop, and only requires using the command line for a few commands.
