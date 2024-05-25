"""This Python code handles account operations, such as logging in and creating an account."""

import flask
import PhoneBook
import hashlib
import uuid

@PhoneBook.app.route("/", methods = ["GET"])
def login_screen():
    """
    Entry point to the application. Checks whether or not the
    user is logged in, either directing them to the main page
    or the login page.
    """

    if "logged_in_user" in flask.session:
        return flask.redirect(flask.url_for("main_page"), **context)
    
    else:
        context = {}
        return flask.render_template("login_page.html", **context)

@PhoneBook.app.route("/logout", methods = ["GET"])
def logout():
    """Logs out the current user and returns them to the login page."""

    del flask.session["logged_in_user"]
    return flask.redirect(flask.url_for("login_screen"))

@PhoneBook.app.route("/check_credentials", methods = ["POST"])
def check_credentials():
    """
    Checks to ensure that the entered username and password are correct,
    logging in the user if so.
    """

    database = PhoneBook.model.get_db()
    context = {}
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")

    username_exists = database.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()
    if username_exists is None:
        flask.flash("Incorrect username or password.")
        return flask.redirect(flask.url_for("login_screen"))

    else:
        correct_password = database.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
        password_data = correct_password["password"].split("$")
        hash = hashlib.new("sha256")
        salt = password_data[1]
        salted_password = salt + password
        hash.update(salted_password.encode("utf-8"))
        password_hash = hash.hexdigest()
        password_db_value = "$".join(["sha256", salt, password_hash])

        correct_credentials = database.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_db_value)).fetchone()

        if correct_credentials is not None:
            flask.session["logged_in_user"] = username
            return flask.redirect(flask.url_for("main_page"))
        
        else:
            flask.flash("Incorrect username or password.", category = "message")
            return flask.redirect(flask.url_for("login_screen"))


@PhoneBook.app.route("/create_account", methods = ["GET"])
def create_account_page():
    """
    Displays the page for a user to create an account.
    """

    context = {}
    return flask.render_template("create_account.html", **context)

@PhoneBook.app.route("/create_user_account", methods = ["POST"])
def create_user_account():
    """
    Attempts to create a new user account.
    """

    database = PhoneBook.model.get_db()
    context = {}
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    confirm_password = flask.request.form.get("confirm_password")

    username_exists = database.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()

    if username_exists is not None:
        flask.flash("This user already exists.")
        context["username"] = username
        return flask.redirect(flask.url_for("create_account_page"))

    elif password != confirm_password:
        flask.flash("Password and confirm password do not match.")
        return flask.redirect(flask.url_for("create_account_page"))
    
    else:
        salt = uuid.uuid4().hex
        hash = hashlib.new("sha256")
        salted_password = salt + password
        hash.update(salted_password.encode("utf-8"))
        password_hash = hash.hexdigest()
        password_db_value = "$".join(["sha256", salt, password_hash])

        database.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password_db_value))
        return flask.redirect(flask.url_for("login_screen"))