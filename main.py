import os
from math import ceil

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from tools.db_service import DbService
from tools.parse_ese import ParseInternetExplorer
from tools.parse_sqlite import ParseFirefox, ParseChrome

app = Flask(__name__)

UPLOAD_FOLDER = 'upload/'
DATABASE = "Linkcollection.sqlite"
MAX_ROWS_PAGE = 50
has_uploaded = False
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
            "Versand und Logistik",
            "Messenger",
            "Onion-Link",
            "Andere"
        ]
url_collection = []
uploaded_filename = ""
db_service = DbService(DATABASE)

@app.route('/', methods=["GET", "POST"])
def index():
    global has_uploaded
    if request.method == "GET":
        has_uploaded = len(os.listdir(app.config["UPLOAD_PATH"])) > 0

        # Filter arguments
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        try:
            show_uncategorized = bool(request.args.get("show_uncategorized"))
        except:
            show_uncategorized = False
        try:
            filter_by_name = request.args.get("namefilter")
        except:
            filter_by_name = None

        not_category_filter = None
        category_filter = None
        if not show_uncategorized:
            not_category_filter = ""

        pages = ceil(db_service.get_entries_count(filter_by_name, category_filter, not_category_filter) / MAX_ROWS_PAGE)
        offset = (page - 1) * MAX_ROWS_PAGE

        url_collection = db_service.get_entries_with_filter(filter_by_name, category_filter, not_category_filter, offset, MAX_ROWS_PAGE)

        return render_template("home.html",
                               url_collection=url_collection,
                               categories=categories,
                               has_uploaded=has_uploaded,
                               pages=pages)
    else:
        urls = request.form.getlist("url")
        category_list = request.form.getlist("categories")
        db_service.write_entry(urls, category_list)
        return redirect(request.url)


@app.route("/upload", methods=["POST"])
def upload_file():
    global has_uploaded
    global uploaded_filename
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
        has_uploaded = True
        uploaded_filename = filename
        parser = None
        if filename == "places.sqlite":
            parser = ParseFirefox(os.path.join(app.config['UPLOAD_PATH'], uploaded_filename))
        elif filename == "History":
            parser = ParseChrome(os.path.join(app.config['UPLOAD_PATH'], uploaded_filename))
        elif filename == "WebCacheV01.dat":
            parser = ParseInternetExplorer(os.path.join(app.config["UPLOAD_PATH"], uploaded_filename))
        else:
            delete_file()
        # TODO: Show error
        if parser is not None:
            url_collection = parser.get_history_urls()
            db_service.write_entry_with_no_category(url_collection)
        return redirect(request.url_root)


@app.route("/delete", methods=["POST"])
def delete_file():
    global uploaded_filename
    global has_uploaded
    try:
        if uploaded_filename == "":
            uploaded_filename = os.listdir(app.config["UPLOAD_PATH"])[0]
        os.remove(os.path.join(app.config['UPLOAD_PATH'], uploaded_filename))
    except:
        return redirect("/")
    uploaded_filename = ""
    has_uploaded = False
    return redirect("/")


if __name__ == "__main__":
    exists = os.path.exists(UPLOAD_FOLDER)
    if not exists:
        os.makedirs(UPLOAD_FOLDER)
    app.config["DATABASE"] = DATABASE
    app.config["UPLOAD_PATH"] = UPLOAD_FOLDER
    app.run(host="0.0.0.0", port=9999, debug=True)