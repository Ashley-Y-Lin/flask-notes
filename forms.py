"""Forms for flask notes."""

from wtforms import StringField, EmailField, PasswordField, TextAreaField
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


class AddNewNoteForm(FlaskForm):
    """Form for adding a new note."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])

    content = TextAreaField("Content", validators=[InputRequired()])


class EditNoteForm(FlaskForm):
    """Form for editing an existing note."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])

    content = TextAreaField("Content", validators=[InputRequired()])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection for delete"""
