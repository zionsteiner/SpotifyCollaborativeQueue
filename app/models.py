from app import db


class SpotifyCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, index=True, unique=True)
    access_token = db.Column(db.String, index=True, unique=True)
    expires_at = db.Column(db.Integer, index=True, unique=False)
    refresh_token = db.Column(db.String, index=True, unique=True)
    code = db.Column(db.String, index=True, unique=True)
