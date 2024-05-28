"""
This Python code handles account operations, such as logging in and creating an account.
"""

import flask
import PhoneBook
import hashlib
import uuid
import os


@PhoneBook.app.route("/", methods = ["GET"])
def login_screen():
    """
    Checks whether or not the user is logged in,
    either directing them to the main page
    or the login page.
    """

    if "logged_in_user" in flask.session:
        return flask.redirect(flask.url_for("main_page"))

    else:
        context = {}
        return flask.render_template("login_page.html", **context)


@PhoneBook.app.route("/logout", methods = ["GET"])
def logout(message = ""):
    """
    Logs out the current user and returns them to the login page.
    """

    if "logged_in_user" not in flask.session:
        flask.flash("You must be logged in to view that page.")
        return flask.redirect(flask.url_for("login_screen"))

    flask.session.clear()

    if message == "delete account":
        flask.flash("Account successfully deleted.")

    return flask.redirect(flask.url_for("login_screen"))


@PhoneBook.app.route("/check_credentials", methods = ["POST"])
def check_credentials():
    """
    Checks to ensure that the entered username and password are correct,
    logging in the user if so.
    """

    if "logged_in_user" not in flask.session:
        flask.flash("You must be logged in to perform that functionality.")
        return flask.redirect(flask.url_for("login_screen"))

    database = PhoneBook.model.get_db()
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

    if "logged_in_user" not in flask.session:
        flask.flash("You must be logged in to perform that functionality.")
        return flask.redirect(flask.url_for("login_screen"))

    database = PhoneBook.model.get_db()
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    first_name = flask.request.form.get("first_name")
    last_name = flask.request.form.get("last_name")
    confirm_password = flask.request.form.get("confirm_password")

    username_exists = database.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()

    if username_exists is not None:
        flask.flash("This user already exists.")
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

        database.execute("INSERT INTO users(username, password, first_name, last_name) VALUES (?, ?, ?, ?)",
                         (username, password_db_value, first_name, last_name))

        flask.flash("Account successfully created! Please login.")
        return flask.redirect(flask.url_for("login_screen"))


@PhoneBook.app.route("/change_account", methods = ["GET"])
def change_account():
    """
    Displays the UI for allowing a user to either change their password or
    delete their account.
    """

    if "logged_in_user" not in flask.session:
        flask.flash("You must be logged in to view that page.")
        return flask.redirect(flask.url_for("login_screen"))

    else:
        delete = flask.request.args.get("delete", default = "no")
        previous_page = flask.request.args.get("previous_page")
        context = {"delete": delete, "previous_page": previous_page}

        return flask.render_template("edit_account.html", **context)


@PhoneBook.app.route("/change_password", methods = ["POST"])
def change_password():
    """
    Allows the user to change the password to their account.
    """

    if "logged_in_user" not in flask.session:
        flask.flash("You must be logged in to perform that functionality.")
        return flask.redirect(flask.url_for("login_screen"))

    old_password = flask.request.form.get("old_password")
    new_password = flask.request.form.get("new_password")
    confirm_new_password = flask.request.form.get("confirm_new_password")

    database = PhoneBook.model.get_db()
    correct_password = database.execute("SELECT password FROM users WHERE username = ?",
                                        (flask.session["logged_in_user"],)).fetchone()
    password_data = correct_password["password"].split("$")

    salt = password_data[1]
    hash = hashlib.new("sha256")
    salted_password = salt + old_password
    hash.update(salted_password.encode("utf-8"))
    password_hash = hash.hexdigest()
    password_db_value = "$".join(["sha256", salt, password_hash])

    correct_credentials = database.execute("SELECT * FROM users WHERE username = ? AND password = ?", (flask.session["logged_in_user"], password_db_value)).fetchone()

    if correct_credentials is not None and new_password == confirm_new_password:
        new_salt = uuid.uuid4().hex
        new_hash = hashlib.new("sha256")
        new_salted_password = new_salt + new_password
        new_hash.update(new_salted_password.encode("utf-8"))
        new_password_hash = new_hash.hexdigest()
        new_password_db_value = "$".join(["sha256", new_salt, new_password_hash])

        database.execute("UPDATE users SET password = ? WHERE username = ?", (new_password_db_value, flask.session["logged_in_user"]))
        flask.flash("Password successfully changed.")
        return flask.redirect(flask.url_for("main_page"))

    elif correct_credentials is not None and new_password != confirm_new_password:
        flask.flash("New password and confirm new password do not match.")
        return flask.redirect(flask.url_for("change_account"))

    elif correct_credentials is None:
        flask.flash("Old password is incorrect.")
        return flask.redirect(flask.url_for("change_account"))


@PhoneBook.app.route("/delete_account", methods = ["POST"])
def delete_account():
    """
    Deletes the logged in user's account.
    """

    if "logged_in_user" not in flask.session:
        flask.flash("You must be logged in to perform that functionality.")
        return flask.redirect(flask.url_for("login_screen"))

    else:
        database = PhoneBook.model.get_db()
        profile_pictures_delete = database.execute("SELECT profile_picture FROM contacts WHERE contact_owner = ?",
                                                   (flask.session["logged_in_user"],)).fetchall()

        for picture in profile_pictures_delete:
            if picture["profile_picture"] != "":
                os.remove(PhoneBook.app.config["UPLOAD_FOLDER"]/picture["profile_picture"])

        database.execute("DELETE FROM contacts WHERE contact_owner = ?", (flask.session["logged_in_user"],))
        database.execute("DELETE FROM users WHERE username = ?", (flask.session["logged_in_user"],))
        return logout("delete account")
