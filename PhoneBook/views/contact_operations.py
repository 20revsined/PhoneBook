import flask
import PhoneBook

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

    decision = flask.request.form.get("selection")
    context = {}

    if decision == "create":
        return flask.render_template("add_contact.html", **context)

    elif decision == "delete":
        return flask.render_template("delete_contact.html", **context)

    elif decision == "update":
        return flask.render_template("update_contact.html", **context)
    
    elif decision == "view":
        return flask.redirect(flask.url_for("view_contacts"))

@PhoneBook.app.route("/update_contact", methods = ["GET"])
def update_contact():
    """Allows the user to update one of their contacts in the phonebook."""

    context = {}
    return flask.render_template("update_contact.html", **context)

@PhoneBook.app.route("/view_contacts", methods = ["GET"])
def view_contacts():
    """Allows the user to view their current contacts in their phonebook."""

    context = {}
    database = PhoneBook.model.get_db()
    contacts = database.execute("SELECT * FROM contacts WHERE contact_owner = ?",
                                    (flask.session["logged_in_user"],)).fetchall()
        
    context["num_contacts"] = len(contacts)
    context["contacts"] = contacts

    return flask.render_template("view_contacts.html", **context)