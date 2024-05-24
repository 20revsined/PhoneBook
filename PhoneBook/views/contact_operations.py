import flask
import PhoneBook

@PhoneBook.app.route("/main", methods = ["GET"])
def main_page():
    if "logged_in_user" not in flask.session:
        return flask.redirect(flask.url_for("login_screen"))
    
    else:
        context = {}
        return flask.render_template("main_page.html", **context)