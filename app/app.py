import os
import pathlib

import db
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

OSM_FILES = pathlib.Path("osm_files")


def get_osm_files():
    return sorted(os.listdir(pathlib.Path(__file__).parent / "osm_files"))


@app.route("/")
def home(errors=None):
    if errors is None:
        errors = []
    template_name = "_index.html" if request.headers.get("HX-Request") else "index.html"
    return render_template(
        template_name,
        osm_files=get_osm_files(),
        databases=db.get_all_databases(),
        errors=errors,
        host=db.LOCAL_POSTGRES_HOST,
        port=db.LOCAL_POSTGRES_PORT,
        user=db.POSTGRES_USER,
        password=db.POSTGRES_PASSWORD,
    )


@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["osm_file"]
    filename = secure_filename(f.filename)
    path = OSM_FILES / filename
    if not path.exists():
        f.save(path)
    elif filename:
        i = 1
        while (nonconflicting_path := path.with_stem(f"{path.stem}-{i}")).exists():
            i += 1
        f.save(nonconflicting_path)
    return home()


@app.route("/delete-file/<string:file_name>", methods=["DELETE"])
def delete_file(file_name):
    path = OSM_FILES / file_name
    path.unlink(missing_ok=True)
    return home()


@app.route("/create-db-from-file", methods=["POST"])
def create_db_from_file():
    data = request.form
    db_name = data.get("db_name").replace(" ", "_")
    if db_name == "":
        return home()
    path = OSM_FILES / data.get("file_name")
    try:
        db.import_osm(str(path), db_name)
    except Exception as e:
        if hasattr(e, "pgcode") and e.pgcode == "42P04":
            return home(errors=["A database with that name already exists. Please choose a different name."])
        raise e
    return home()


@app.route("/drop-db/<string:db_name>", methods=["DELETE"])
def drop_db(db_name):
    try:
        db.drop_db(db_name)
    except Exception as e:
        if hasattr(e, "pgcode") and e.pgcode == "55006":
            return home(
                errors=[
                    "This database is in use, it cannot be deleted. Ensure there are no active connections "
                    "to the database to delete it."
                ]
            )
    return home()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
