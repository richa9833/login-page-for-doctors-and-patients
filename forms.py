from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, RadioField, FileField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

class SignupForm(FlaskForm):
    role = RadioField(
        "I am a",
        choices=[("P", "Patient"), ("D", "Doctor")],
        default="P",
        validators=[DataRequired()],
    )
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=80)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=80)])
    profile_image = FileField("Profile Picture (optional)")
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=80),
            Regexp(r"^[A-Za-z0-9_.-]+$", message="Only letters, numbers, . _ -"),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, message="Use at least 6 characters")],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    address_line1 = StringField("Address Line 1", validators=[DataRequired(), Length(max=255)])
    city = StringField("City", validators=[DataRequired(), Length(max=80)])
    state = StringField("State", validators=[DataRequired(), Length(max=80)])
    pincode = StringField("Pincode", validators=[DataRequired(), Length(min=4, max=12)])

    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
