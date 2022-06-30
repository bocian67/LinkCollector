from flask import Flask, render_template

app = Flask(__name__)

# TODO Pagination: https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e

@app.route('/')
def index():
    url_collection = [
        "google.com",
        "baidu.com",
        "yandex.ru",
        "bing.com",
        "duckduckgo.com",
        "google.com.br",
        "google.de",
        "google.co.jp",
        "google.co.uk",
        "daum.net",
        "predictiondexchange.com",
        "google.it",
        "seznam.cz",
        "google.fr",
        "google.co.in",
        "google.es",
        "music.youtube.com"
    ]
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
    return render_template("home.html", url_collection=url_collection, categories=categories)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)