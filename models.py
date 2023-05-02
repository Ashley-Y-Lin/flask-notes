"""Models for Flask Notes app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    """User."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    # TODO: implement error handling for duplicate emails
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


class Note(db.Model):
    """Note."""

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # TODO: always have a default of empty string if nullable = false
    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    owner_username = db.Column(db.String(20), db.ForeignKey("users.username"))

    user = db.Relationship("User", backref="notes")


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)
