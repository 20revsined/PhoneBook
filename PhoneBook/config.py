"""
PhoneBook development configuration.
"""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b"\x0b\x7f\x89\xb6P\x90\x13\x89\x92\x86\xf5rS\xff\x92\xb6\xaeF\xae;\x9fSpQ"
SESSION_COOKIE_NAME = 'login'
PHONEBOOK_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = PHONEBOOK_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/phonebook.sqlite3
DATABASE_FILENAME = PHONEBOOK_ROOT/'var'/'phonebook.sqlite3'
