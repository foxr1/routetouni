import os

from flask import Flask, render_template, send_from_directory

from news_and_revision import web_scraper, revision

import firebase_admin
from firebase_admin import db

app = Flask(__name__)


firebase_admin.initialize_app(options={
    'databaseURL': 'https://route2uni-default-rtdb.firebaseio.com/'
})


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/gregister')
def gregister():
    return render_template("google_login.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/news_feed')
def news_feed():
    news_list = web_scraper.main()
    revision_list = revision.main()
    return render_template("news_feed.html")


if __name__ == '__main__':
    app.run(debug=True)
