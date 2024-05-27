"""PhoneBook package initializer."""

import flask

app = flask.Flask(__name__)
app.config.from_object('PhoneBook.config')
app.config.from_envvar('PHONEBOOK_SETTINGS', silent=True)

import PhoneBook.views
import PhoneBook.model
