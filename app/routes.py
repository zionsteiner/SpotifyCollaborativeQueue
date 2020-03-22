import requests
from flask import render_template, redirect, url_for, request
from app import app, db, sp_oauth
from app.forms import CodeInputForm, SongEntryForm
import spotipy
import random
import time
import string
from app.models import SpotifyCredentials


@app.route('/', methods=['GET', 'POST'])
def home():
    form = CodeInputForm()
    if form.validate_on_submit():
        return redirect(url_for('queue', code=form.session_code.data))
    return render_template('home.html', form=form)


@app.route('/login')
def login():
    code = None
    access_token = None

    while not code:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            # Token info
            token_info = sp_oauth.get_access_token(code, check_cache=False)
            access_token = token_info['access_token']
            expires_at = token_info['expires_in'] + time.time()
            refresh_token = token_info['refresh_token']

            # Get username
            sp = spotipy.Spotify(access_token)
            user_id = sp.current_user()['id']

            # Update existing cred entry if one exists
            existing_cred = SpotifyCredentials.query.filter_by(user_id=user_id).first()
            if existing_cred:
                existing_cred.access_token = token_info['access_token']
                existing_cred.expires_at = token_info['expires_in'] + time.time()
                existing_cred.refresh_token = token_info['refresh_token']

                db.session.commit()
            # Add new cred entry
            else:
                # Generate random access code
                chars = set(string.ascii_letters) | set(string.digits)
                access_code = ''.join([random.choice(list(chars)) for _ in range(10)])

                cred = SpotifyCredentials(user_id=user_id,
                                          access_token=access_token,
                                          expires_at=expires_at,
                                          refresh_token=refresh_token,
                                          code=access_code)
                db.session.add(cred)
                db.session.commit()

            return redirect(url_for('view_code', code=access_code))
        else:
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)


# ToDo: add option to edit access code
@app.route('/view_code')
def view_code():
    code = request.args['code']
    return render_template('view_code.html', code=code)


@app.route('/queue/<string:code>', methods=['GET', 'POST'])
def queue(code):
    cred = SpotifyCredentials.query.filter_by(code=code).first()
    if not cred:
        return f'No listening party with code {code}'

    # Refresh credentials is needed
    is_expired = cred.expires_at < time.time() + 60
    if is_expired:
        # Update cred in db
        token_info = sp_oauth.refresh_access_token(cred.refresh_token)
        cred.access_token = token_info['access_token']
        cred.expires_at = token_info['expires_in'] + time.time()
        cred.refresh_token = token_info['refresh_token']
        db.session.commit()

    form = SongEntryForm()
    if form.validate_on_submit():
        song = form.name.data
        artist = form.artist.data

        sp = spotipy.Spotify(cred.access_token)
        results = sp.search(song + ' ' + artist)
        if results.get('tracks', None).get('items', None):
            song_uri = results['tracks']['items'][0]['uri']
            sp.add_to_queue(song_uri)
            return render_template('queue.html', form=form, msg='Song added to queue')
        else:
            return render_template('queue.html', form=form, msg='Song not found')
    else:
        return render_template('queue.html', form=form)