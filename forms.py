from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import InputRequired, NumberRange

class CupcakeForm(FlaskForm):
    flavor = StringField("Flavor", validators=[InputRequired(message="Cupcake flavor cannot be empty")])
    size = SelectField("Size", choices=["Small", "Medium", "Large"])
    rating = FloatField("Rating", validators=[NumberRange(min=1, max=10, message="Rating should be between 1 and 10")])
    image = StringField("Image")
