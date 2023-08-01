# Fibonacci Calculator

Updated: August 1st 2023

# Live Application

The project is hosted live on Heroku at
[https://fibonacci-calculator-2531b1231971.herokuapp.com/](https://fibonacci-calculator-2531b1231971.herokuapp.com/)

# Introduction

Simple Fibonacci Calculator done for the Chan-Zuckerberg Biohub challenge

# Instruction

# If downloading on local machine

1. Go to the folder in fibonacci-calculator
2. Open a console and create a virtual environment `python3 -m venv venv`
3. Activate the environment using `source venv/bin/activate`, you should now see (venv) or (main)
4. Install all dependencies `pip install -r requirements.txt`

Your directory should look like this
```
.fibonacci-calculator-app/
├── static/
├── templates/
├── venv/
|
├── .gitignore
├── app.py
├── fibonacci.db
├── README
└── requirements.txt
```
# Database setup

# We will be using SQlite3 which is a very light weight relational database to store our results

5. Open a new bash console, run the command `sqlite3 fibonacci.db`, you will enter the database shell
6. To clear the tables, run the command `DROP TABLE fibonacci;`.

# You are now ready to run the application

7. Inside the console with virtual environment, run `python app.py` and open localhost:5000 on your browser.
8. Enter a number, click generate and it will redirect you to the results page.

# If you enter the same number again, it will calculate much faster since the results are already stored in the database!
