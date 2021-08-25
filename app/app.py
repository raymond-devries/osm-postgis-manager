import os
import pathlib

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")
def home():
    print(os.listdir(pathlib.Path(__file__).parent / "osm_files"))
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["osm_file"]
        filename = secure_filename(f.filename)
        f.save(f"osm_files/{filename}")
        return home()
