from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class inputGPS(FlaskForm):
    street = StringField('Enter Your Street Name + Number',validators=[DataRequired(),  Length(min=2, max=20)])
    city = StringField('Enter Your City',validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Locate Me A Bike!')