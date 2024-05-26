import flask
import PhoneBook
import uuid
import pathlib
import os

def save_file(fileobj, filename):
    """Generates a unique filename to save a user's profile picture in the database."""
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    new_file_name = f"{stem}{suffix}"
    file_path = PhoneBook.app.config["UPLOAD_FOLDER"]/new_file_name
    fileobj.save(file_path)

    return new_file_name

@PhoneBook.app.route("/uploads/<path:filename>", methods = ["GET"])
def return_profile_picture(filename):
    """Attempts to return the profile_picture of a given contact."""
    if "logged_in_user" not in flask.session and filename != "phonebook_icon.png":
        return flask.redirect(flask.url_for("login_screen"))
    
    else:
        try:
            return flask.send_from_directory(PhoneBook.app.config["UPLOAD_FOLDER"], filename)
        except FileNotFoundError:
            flask.flash("One or more profile pictures couldn't be found.")
            return flask.redirect(flask.url_for("main_page"))

@PhoneBook.app.route("/main", methods = ["GET"])
def main_page():
    """This returns the UI that the user sees after logging in."""

    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))
    
    else:
        context = {"logged_in_user": flask.session["logged_in_user"]}
        return flask.render_template("main_page.html", **context)
    
@PhoneBook.app.route("/operation", methods = ["POST"])
def operation():
    """This function returns the appropriate page based on
    what the user wants to do."""

    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))

    decision = flask.request.form.get("selection")
    
    if decision == "create":
        return flask.redirect(flask.url_for("add_contact_page"))

    elif decision == "delete":
        return flask.redirect(flask.url_for("delete_contact_page"))

    elif decision == "update":
        return flask.redirect(flask.url_for("update_contact_page"))
    
    elif decision == "view":
        return flask.redirect(flask.url_for("view_contacts"))

@PhoneBook.app.route("/add_contact", methods = ["GET"])
def add_contact_page():
    """Displays the UI for adding a contact to the phone book."""

    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))

    context = {}
    return flask.render_template("add_contact.html", **context)

@PhoneBook.app.route("/create_contact", methods = ["POST"])
def create_contact():
    """Adds a contact to the user's list of contacts in the phone book."""
    database = PhoneBook.model.get_db()

    first_name = flask.request.form.get("first_name")
    last_name = flask.request.form.get("last_name")
    profile_picture = flask.request.files.get("profile_picture")
    phone_number = flask.request.form.get("phone_number")
    email_address = flask.request.form.get("email_address")
    home_address = flask.request.form.get("home_address")

    profile_exists = database.execute("SELECT * FROM contacts WHERE contact_owner = ? AND first_name = ? AND last_name = ? AND phone_number = ?", (flask.session["logged_in_user"], first_name, last_name, phone_number)).fetchone()

    if profile_exists is not None:
        print(profile_exists["first_name"])
        flask.flash("This contact already exists.")
        return flask.redirect(flask.url_for("add_contact_page"))
    
    else:
        profile_picture_name = profile_picture.filename
        new_file_name = save_file(profile_picture, profile_picture_name)
        database.execute("INSERT INTO contacts(contact_owner, first_name, last_name, profile_picture, phone_number, email_address, home_address) VALUES (?, ?, ?, ?, ?, ?, ?)", (flask.session["logged_in_user"], first_name, last_name, new_file_name, phone_number, email_address, home_address))
        flask.flash("Contact successfully added!")
        return flask.redirect(flask.url_for("main_page"))

@PhoneBook.app.route("/delete_contact", methods = ["GET"])
def delete_contact_page():
    """Displays the UI for deleting a contact from the phone book."""

    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))
    
    database = PhoneBook.model.get_db()
    context = {}
    contacts = database.execute("SELECT * FROM contacts WHERE contact_owner = ?",
                                    (flask.session["logged_in_user"],)).fetchall()
    
    context["num_contacts"] = len(contacts)
    context["contacts"] = contacts
    
    return flask.render_template("delete_contact.html", **context)

@PhoneBook.app.route("/remove_contact", methods = ["POST"])
def remove_contact():
    """Delete a contact from the phone book."""

    database = PhoneBook.model.get_db()
    first_name = flask.request.form.get("first_name")
    last_name = flask.request.form.get("last_name")
    phone_number = flask.request.form.get("phone_number")

    valid_entry = database.execute("SELECT * FROM contacts WHERE contact_owner = ? AND first_name = ? AND "
                                   "last_name = ? AND phone_number = ?", (flask.session["logged_in_user"],
                                    first_name, last_name, phone_number)).fetchone()
    if valid_entry is not None:
        profile_picture = database.execute("SELECT profile_picture FROM contacts WHERE contact_owner = ? AND id = ?",
                                           (flask.session["logged_in_user"], valid_entry["id"])).fetchone()
        os.remove(PhoneBook.app.config["UPLOAD_FOLDER"]/profile_picture["profile_picture"])
        
        database.execute("DELETE FROM contacts WHERE contact_owner = ? AND id = ?",
                         (flask.session["logged_in_user"], valid_entry["id"]))
        flask.flash("Contact entry successfully deleted.")
        return flask.redirect(flask.url_for("main_page"))
    else:
        flask.flash("Unable to delete this entry from the phone book. "
        "Please ensure that you are the owner of this contact and have entered the data in the text boxes correctly.")
        return flask.redirect(flask.url_for("delete_contact_page"))

@PhoneBook.app.route("/update_contact_page", methods = ["GET"])
def update_contact_page():
    """Allows the user to update one of their contacts in the phone book."""

    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))

    database = PhoneBook.model.get_db()
    context = {}
    contacts = database.execute("SELECT * FROM contacts WHERE contact_owner = ?",
                                    (flask.session["logged_in_user"],)).fetchall()
    
    context["num_contacts"] = len(contacts)
    context["contacts"] = contacts
    return flask.render_template("update_contact.html", **context)

@PhoneBook.app.route("/update_contact", methods = ["POST"])
def update_contact():
    """Allows the user to update a contact in the phone book."""
    database = PhoneBook.model.get_db()

    old_first_name = flask.request.form.get("old_first_name")
    old_last_name = flask.request.form.get("old_last_name")
    old_phone_number = flask.request.form.get("old_phone_number")

    contact_exists = database.execute("SELECT * FROM contacts WHERE contact_owner = ? AND first_name = ?"
                                      "AND last_name = ? AND phone_number = ?",
                            (flask.session["logged_in_user"], old_first_name, old_last_name, old_phone_number)).fetchone()
    
    if contact_exists is not None:
        new_first_name = flask.request.form.get("new_first_name")
        new_last_name = flask.request.form.get("new_last_name")
        new_profile_picture = flask.request.files.get("new_profile_picture")
        new_phone_number = flask.request.form.get("new_phone_number")
        new_email_address = flask.request.form.get("new_email_address")
        new_home_address = flask.request.form.get("new_home_address")

        contact_info_changed = False

        if new_first_name is not None and new_first_name != "":
            database.execute("UPDATE contacts SET first_name = ? WHERE contact_owner = ? AND id = ?",
                             (new_first_name, flask.session["logged_in_user"], contact_exists["id"]))
            contact_info_changed = True
        
        if new_last_name is not None and new_last_name != "":
            database.execute("UPDATE contacts SET last_name = ? WHERE contact_owner = ? AND id = ?",
                             (new_last_name, flask.session["logged_in_user"], contact_exists["id"]))
            contact_info_changed = True

        if new_profile_picture is not None and new_profile_picture.filename != "":
            old_profile_picture = database.execute("SELECT profile_picture FROM contacts WHERE contact_owner = ? AND id = ?",
                                    (flask.session["logged_in_user"], contact_exists["id"])).fetchone()

            os.remove(PhoneBook.app.config["UPLOAD_FOLDER"]/old_profile_picture["profile_picture"])

            new_profile_picture_name = new_profile_picture.filename
            new_file_name = save_file(new_profile_picture, new_profile_picture_name)
            database.execute("UPDATE contacts SET profile_picture = ? WHERE contact_owner = ? and id = ?",
                             (new_file_name, flask.session["logged_in_user"], contact_exists["id"]))
            
            contact_info_changed = True

        if new_phone_number is not None and new_phone_number != "":
            database.execute("UPDATE contacts SET phone_number = ? WHERE contact_owner = ? AND id = ?",
                             (new_phone_number, flask.session["logged_in_user"], contact_exists["id"]))
            contact_info_changed = True

        if new_email_address is not None and new_email_address != "":
            database.execute("UPDATE contacts SET email_address = ? WHERE contact_owner = ? AND id = ?",
                             (new_email_address, flask.session["logged_in_user"], contact_exists["id"]))
            contact_info_changed = True

        if new_home_address is not None and new_home_address != "":
            database.execute("UPDATE contacts SET home_address = ? WHERE contact_owner = ? AND id = ?",
                             (new_home_address, flask.session["logged_in_user"], contact_exists["id"]))
            contact_info_changed = True

        if contact_info_changed:
            flask.flash("Contact successfully updated.")
            return flask.redirect(flask.url_for("main_page"))
        
        else:
            flask.flash("Contact not updated.")
            return flask.redirect(flask.url_for("main_page"))

    else:
        flask.flash("Could not find this contact. Please ensure that you've entered the information correctly.")
        return flask.redirect(flask.url_for("update_contact_page"))

@PhoneBook.app.route("/view_contacts", methods = ["GET"])
def view_contacts():
    """Allows the user to view their current contacts in their phone book."""

    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))

    context = {}
    database = PhoneBook.model.get_db()
    contacts = database.execute("SELECT * FROM contacts WHERE contact_owner = ?",
                                    (flask.session["logged_in_user"],)).fetchall()
    
    contacts = sorted(contacts, key = lambda x: x["last_name"])
    context["num_contacts"] = len(contacts)
    context["contacts"] = contacts

    return flask.render_template("view_contacts.html", **context)
