from flask import Flask, session, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note

from forms import (
    AddNewUserForm,
    LoginUserForm,
    CSRFProtectForm,
    AddNewNoteForm,
    EditNoteForm,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

app.config["SECRET_KEY"] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

"""Flask app for Flask Notes"""
### Authentication functions ###

def authenticate_login(f):
    def wrapper():
        if "username" not in session:
            flash("You must be logged in to view page!")
            return redirect("/")
        # elif session["username"] != username:
        #     flash("Unauthorized user!")
        #     return redirect("/")
    return wrapper


#### Authentication Routes ###


@app.get("/")
def redirect_register():
    """Redirect to /register."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Produce register form or handle register."""

    # Redirect if already logged in
    if "username" in session:
        username = session["username"]
        return redirect(f"/users/{username}")

    form = AddNewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # creates a new user instance
        user = User.register(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    # Redirect if already logged in
    if "username" in session:
        username = session["username"]
        return redirect(f"/users/{username}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.post("/logout")
def logout_user():
    """Log the user out and redirect to /."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        print("\n\n\nworking\n\n\n")
        session.pop("username", None)

    return redirect("/")


### User Routes ###

@authenticate_login
@app.get("/users/<username>")
def display_user_info(username):
    """Display information about the user with the given username.
    Ensure users are logged in to see the page, else redirect to /login."""

    user = User.query.get_or_404(username)
    form = CSRFProtectForm()

    return render_template("user-info.html", user=user, notes=user.notes, form=form)


@app.post("/users/<username>/delete")
def delete_user(username):
    """Deletes user from database and redirects to /"""
    form = CSRFProtectForm()

    if form.validate_on_submit():
        user = User.query.get_or_404(username)

        notes = Note.query.filter(Note.owner_username == username).delete()

        db.session.delete(user)
        db.session.commit()

        session.pop("username", None)

        flash(f"{user.first_name} {user.last_name} deleted")

    return redirect("/")


### NOTES ROUTES ###

@authenticate_login
@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def display_or_add_note(username):
    """Produce add note form or handles add note form submission."""

    form = AddNewNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(
            title=title,
            content=content,
            owner_username=username,
        )

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("add-note.html", form=form)

@authenticate_login
@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def edit_or_update_note(note_id):
    """Produce edit note form or handles edit note form submission."""

    note = Note.query.get_or_404(note_id)
    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    return render_template("edit-note.html", form=form, note=note)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Deletes note from database and redirects to /users/<username>"""
    form = CSRFProtectForm()

    note = Note.query.get_or_404(note_id)

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        flash(f"{note.title} was deleted!")

    return redirect(f"/users/{note.owner_username}")
