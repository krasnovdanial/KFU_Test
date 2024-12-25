# forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import Optional

class FilterForm(FlaskForm):
    operator = SelectField('Оператор', choices=[], validators=[Optional()])
    location = StringField('Локация', validators=[Optional()])
    well_status = SelectField('Активность скважины', choices=[('', 'Любая'), ('active', 'Active'), ('inactive', 'Inactive')], validators=[Optional()])
    submit = SubmitField('Filter')
