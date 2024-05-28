# PhoneBook Web Application

This is a phone book web application that allows users to create theur own account in order to
create, update, view, and delete their contacts in an online phone book.

The app uses HTML for the frontend and Python and SQLite for the backend.

## Getting Started
Note: This installation assumes that you have at least Python >= 3.10 installed on your computer.
If not, please install a Python version >= 3.10.

This installation also assumes that you are familiar with using your computer's command line,
since you will be using it for the setup of this app.

1. Clone this repository by typing `git clone git@github.com:20revsined/PhoneBook.git` (using SSH)
or `git clone https://github.com/20revsined/PhoneBook.git` (using the web URL) - whichever works for you.
If you prefer the GitHub CLI, using the following command: `gh repo clone 20revsined/PhoneBook`.

2. After opening the files in an IDE, run the following command: `chmod +x bin/phonebook_install`, which will make the phonebook_install
script executable. This will allow you to run this script, which will install the necessary dependencies for this project.

3. Then, run the following command, `./bin/phonebook_install`, which will run the `phonebook_install` shell script.
If you run `python3 --version`, and your version is less than 3.10, see lines 7 and 8 in `phonebook_install` for a
workaround.

4. After installing of the necessary dependencies and the app itself, enter the virtual environment by typing:
`source phonebook/env/activate`. You can leave the environment at any time by typing `deactivate` in your command line.

5. To run the app, run the following command: `./bin/phonebook_run`. To stop running the app, hit control + C in
your command line.

## Important Note
Please do not store any sensitive information in the database.

If you plan to add your own data to the `sample_data.sql` file, use empty strings (`""`) when inserting
data for the `profile_picture` column if you do not want to use a profile picture.
