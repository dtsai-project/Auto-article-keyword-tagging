from flask_wtf import FlaskForm
from wtforms import StringField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class Post(FlaskForm):
    title = StringField('Judul', validators=[DataRequired()])
    content = TextAreaField('Isi', validators=[DataRequired()])
    submit = SubmitField('Tambah Artikel')
