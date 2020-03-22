from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from spotipy import oauth2
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

sp_oauth = oauth2.SpotifyOAuth(app.config['SPOTIFY_CLIENT_ID'],
                                   app.config['SPOTIFY_CLIENT_SECRET'],
                                   app.config['REDIRECT_URI'],
                                   scope=app.config['SCOPE'])

from app import routes, models