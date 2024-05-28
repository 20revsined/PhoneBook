# PhoneBook Web Application

This is a phone book web application that allows users to create theur own account in order to
create, update, view, and delete their contacts in an online phone book.

The app uses HTML for the frontend and Python and SQLite for the backend.

## Getting Started
Note: This installation assumes that you have at least Python >= 3.10 installed on your computer.
If not, please install a Python version >= 3.10. You can check your version of Python by running
`python3 --version` or `python --version` on your command line.

This installation also assumes that you are familiar with using your computer's command line,
since you will be using it for the setup of this app.

1. Clone this repository by typing `git clone git@github.com:20revsined/PhoneBook.git` (using SSH)
or `git clone https://github.com/20revsined/PhoneBook.git` (using the web URL) on your command line.
If you prefer the GitHub CLI, using the following command: `gh repo clone 20revsined/PhoneBook`.
After cloning, go to the PhoneBook directory by typing `cd PhoneBook` if you aren't already there.

3. After opening the files in an IDE, run the following command on your command line: `chmod +x bin/phonebook_install`, which will make the phonebook_install
script executable. This will allow you to run this script, which will install the necessary dependencies for this project.
If you don't have permission to run this command, run `sudo chmod +x bin/phonebook_install`.

4. Then, run the following command, `./bin/phonebook_install`, which will run the `phonebook_install` shell script.
If you run `python3 --version`, and your version is less than 3.10, see lines 7 and 8 in `phonebook_install` for a
workaround.

5. After installing of the necessary dependencies and the app itself, enter the virtual environment by typing:
`source phonebook/env/activate`. You can leave the environment at any time by typing `deactivate` in your command line.

6. To run the app, run the following command: `./bin/phonebook_run`. To use the app, go to your favorite web browser and type the following for the URL: `localhost:8000`.
If prompted by your computer, make sure to allow incoming connections. To stop running the app, hit control + C in your command line.

## Database Shell Script Information
If you want to reset the stored data in the database back to what it was, type the following
in your command line (make sure you're in the PhoneBook directory): `./bin/phonebook_db reset`.

If you want to delete the database, type the following in your command line (make sure you're in the PhoneBook directory): `./bin/phonebook_db delete`.
Then, type the following to recreate it: `./bin/phonebook_db create` or `./bin/phonebook_db reset`.

## Important Note
Please do not store any sensitive information in the database.

If you plan to add your own data to the `sample_data.sql` file, use empty strings (`""`) when inserting
data for the `profile_picture` column if you do not want to use a profile picture.
