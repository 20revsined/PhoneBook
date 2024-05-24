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
        return flask.redirect(flask.url_for("main_page"))
    
    else:
        context = {"message": False}
        return flask.render_template("login_page.html", **context)

@PhoneBook.app.route("/check_credentials", methods = ["POST"])
def check_credentials():
    """
    Checks to ensure that the entered username and password are correct,
    logging in the user if so.
    """

    database = PhoneBook.model.get_db()
    context = {"message": False}
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")

    username_exists = database.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()
    if username_exists is None:
        context["message"] = True
        return flask.render_template("login_page.html", **context)

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
            context["message"] = True
            return flask.render_template("login_page.html", **context)


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
        context["username"] = username
        return flask.render_template("user_already_exists.html", **context)

    elif password != confirm_password:
        return flask.render_template(flask.url_for("create_account_page"), **context)
    
    else:
        salt = uuid.uuid4().hex
        hash = hashlib.new("sha256")
        salted_password = salt + password
        hash.update(salted_password.encode("utf-8"))
        password_hash = hash.hexdigest()
        password_db_value = "$".join(["sha256", salt, password_hash])

        database.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password_db_value))
        return flask.redirect(flask.url_for("login_screen"))