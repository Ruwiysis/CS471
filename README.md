# Secure Notes System

A small notes website which is built with Flask and SQLite. It has two versions:
- vulnerable/ : a deliberately insecure version for demonstrating Stored XSS (local use only)
- secure/ : the protected version, this is the main version

## Requirements
- Python 3
- Flask (listed in requirements.txt)

## Setup
1. Open a terminal in the project folder.
2. Create a virtual environment: python -m venv venv
3. Activate it (Windows): venv\Scripts\activate
4. Install Flask: pip install -r requirements.txt

## Run the vulnerable version
cd vulnerable
python app.py
Open http://127.0.0.1:5001

## Run the secure version
cd secure
python app.py
Open http://127.0.0.1:5000

## How to use
1. Open /register and create an account.
2. Log in at /login.
3. Add, open and delete your notes.

The database file (notes.db) is created automatically the first time an app runs.

## Warning
The vulnerable folder is intentionally insecure. Run it only on your own computer.