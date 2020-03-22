from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CodeInputForm(FlaskForm):
    session_code = StringField('Session code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SongEntryForm(FlaskForm):
    name = StringField('Song name', validators=[DataRequired()])
    artist = StringField('Artist name', validators=[DataRequired()])
    submit = SubmitField('Submit')
