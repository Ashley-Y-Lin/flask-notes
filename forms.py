"""Forms for flask notes."""

from wtforms import StringField, EmailField, PasswordField
from flask_wtf import FlaskForm

from wtforms.validators import InputRequired, Length


class AddNewUserForm(FlaskForm):
    """Form for adding a new user."""

    username = StringField("Username", validators=[InputRequired(), Length(max=20)])

    password = PasswordField("Password", validators=[InputRequired(), Length(max=100)])

    email = EmailField(
        "Email",
        validators=[
            InputRequired(),
            Length(max=50),
            # TODO: is there a unique validator in WTForms to add here?
        ],
    )

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])

    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginUserForm(FlaskForm):
    """Form for logging in a new user."""

    username = StringField("Username", validators=[InputRequired(), Length(max=20)])

    password = PasswordField("Password", validators=[InputRequired(), Length(max=100)])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection for delete"""
