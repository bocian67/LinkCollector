import os
from math import ceil

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from tools.parse_sqlite import ParseSqlite

app = Flask(__name__)

# TODO Pagination: https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e

UPLOAD_FOLDER = 'upload/'
MAX_ROWS_PAGE = 20
has_uploaded = False
uploaded_filename = ""
categories = [
            "Kunst und Unterhaltung",
            "Dating",
            "E-Mail",
            "Hosting",
            "Suchmaschinen",
            "Social Media",
            "Shopping",
            "Bankwesen",
            "Nachrichten",
            "Erwachsene",
            "Versand und Logistik"
        ]
url_collection = []


@app.route('/', methods=["GET", "POST"])
def index():
    global has_uploaded
    global uploaded_filename
    global url_collection
    directory_content = os.listdir(app.config['UPLOAD_PATH'])
    has_uploaded = len(directory_content) > 0
    if has_uploaded:
        uploaded_filename = directory_content[0]
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            uploaded_filename = filename
            has_uploaded = True
            return redirect(request.url)
    else:
        if has_uploaded and len(url_collection) == 0:
            parser = ParseSqlite(os.path.join(app.config['UPLOAD_PATH'], uploaded_filename))
            url_collection = parser.get_history_urls()
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        pages = ceil(float(len(url_collection)) / MAX_ROWS_PAGE)
        if len(url_collection) >= MAX_ROWS_PAGE:
            start_index = (page - 1) * MAX_ROWS_PAGE
            if len(url_collection[start_index:]) > MAX_ROWS_PAGE:
                end_index = start_index + MAX_ROWS_PAGE
            else:
                end_index = start_index + len(url_collection[start_index:])
            shown_url_collection = url_collection[start_index:end_index]
        else:
            shown_url_collection = url_collection

        return render_template("home.html",
                               url_collection=shown_url_collection,
                               categories=categories,
                               has_uploaded=has_uploaded,
                               pages=pages)


@app.route("/delete", methods=["POST"])
def delete_file():
    global uploaded_filename
    global has_uploaded
    global url_collection
    os.remove(os.path.join(app.config['UPLOAD_PATH'], uploaded_filename))
    uploaded_filename = ""
    has_uploaded = False
    url_collection = []
    return redirect("/")


if __name__ == "__main__":
    exists = os.path.exists(UPLOAD_FOLDER)
    if not exists:
        os.makedirs(UPLOAD_FOLDER)
    app.config["UPLOAD_PATH"] = UPLOAD_FOLDER
    app.run(host="0.0.0.0", port=8080, debug=True)