Running the NUGRAM Web Application

Prerequisites

Ensure you have Python3 installed on your system. You can download it from Python's official website.
Flask and MySQL connector for Python are required. These can be installed using pip:

Unix/Mac:
pip install Flask mysql-connector-python flask-cors

Windows:
py -m pip install Flask mysql-connector-python flask-core

Database Setup

Import the NUGRAM.sql into your MySQL database. This file contains all necessary tables and procedures.
You can use a MySQL Workbench to import the project database or the command line to import the file. For command line, use:

mysql -u [username] -p [password] project < NUGRAM.sql

Configuration

Unix-based Systems (Ubuntu, Mac)

Open a terminal and navigate to the NUGRAM directory:

Step 1: python3 Input_db_creds.py 

Step 2: Start the Flask application:

flask --app app.py run --debug

Step 3:
In a new terminal window, navigate again to the NUGRAM directory and open the login.html in your default browser:

open login.html

Alternatively, you can double-click on the login.html file to open it in your default web browser.


Windows
Open a command prompt and navigate to the NUGRAM directory:

cd path\to\NUGRAM

Open a terminal and navigate to the NUGRAM directory:

Step 1: py Input_db_creds.py (Note: make sure to use python3)

Start the Flask application:

py -m flask --app app.py run --debug

In a new command prompt window, navigate again to the NUGRAM directory and open the login.html in your default browser:

start login.html

As an alternative, you can simply double-click on the login.html file to open it in your default web browser.


Application Credentials:

You can either create a new user, or login into one of our users:

Email: nf@gmail.com
Password: noahpassword

Email: vk@gmail.com
Password: victorpassword





