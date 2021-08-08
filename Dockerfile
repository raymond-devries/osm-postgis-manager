FROM qgis/qgis:latest
RUN apt install osm2pgsql -y
RUN mkdir "app"
COPY app app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
CMD python3 app.py
