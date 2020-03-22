from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from spotipy import oauth2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pxR5xFaq33ytBAg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.dirname(__file__)) + 'app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SPOTIFY_CLIENT_ID'] = '53047d625f1848f79d80c0092ee02489'
app.config['SPOTIFY_CLIENT_SECRET'] = 'e7c233c83cc74124bd861cfde77f0d86'
app.config['REDIRECT_URI'] = 'http://127.0.0.1:5000/login'
app.config['SCOPE'] = 'user-modify-playback-state'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

sp_oauth = oauth2.SpotifyOAuth(app.config['SPOTIFY_CLIENT_ID'],
                                   app.config['SPOTIFY_CLIENT_SECRET'],
                                   app.config['REDIRECT_URI'],
                                   scope=app.config['SCOPE'])

from app import routes, models