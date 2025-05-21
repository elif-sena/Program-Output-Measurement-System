from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, FileField, BooleanField, DateField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class StudentForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    student_number = StringField("Student Number", validators=[DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=100)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    submit = SubmitField("Save")