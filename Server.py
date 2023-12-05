import os
from sqlite3 import dbapi2
from flask import Flask, abort, flash, redirect, request,render_template, url_for
import json
import sqlite3

app = Flask(__name__)

user = None

@app.route("/createAccount", methods=['GET'])
def returnCreateAccount():
    if request.method == 'GET':
        return render_template('Create_Account.html')

@app.route("/mainPage", methods=['GET'])
def returnHome():
    if request.method == 'GET':
        return render_template('Main_Page.html')

def submitNewAccount(firstName,lastName,userName,password):
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute(\
        "INSERT INTO User ('Username', 'FirstName','SurName','Password','Admin') \
        VALUES (?,?,?,?,?)", (userName,firstName,lastName,password,"N"))
        message = True
        conn.commit()
    except Exception as e:
        message = False
        conn.rollback()
    finally:
        conn.close()
        print(message)
        return message

@app.route("/usernameExist", methods = ['POST'])
def usernameExist():
    if request.method == 'POST':
        firstName = request.form.get("firstName").title()
        lastName = request.form.get("lastName").title()
        userName = request.form.get("username")
        password = request.form.get("password")
        try:
            conn = sqlite3.connect('quizDatabase.db')
            cur = conn.cursor()
            cur.execute(\
            "SELECT Username FROM User WHERE Username = ?",([userName]))
            isExist = cur.fetchall()
            cur.close()
            if isExist == []:
                if submitNewAccount(firstName,lastName,userName,password) == True:
                    message = "Welcome to your account, " + firstName
                    global user
                    user = userName
                    return render_template('Account_Details.html', data = message)
                else:
                    message = "Error inserting " + firstName
            else:
                message = "Username '" + userName + "' already exists."
        except Exception as e:
            message = "Error during check"
        return render_template('Create_Account.html', data = message)
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])





def create_table():
    conn = sqlite3.connect('quizDatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            correct_option TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    conn = sqlite3.connect('quizDatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions')
    questions = cursor.fetchall()
    conn.close()
    return render_template('Edit_Quiz.html', questions=questions)

@app.route('/add', methods=['POST'])
def add_question():
    question_text = request.form['question_text']
    option1 = request.form['Answer1']
    option2 = request.form['Answer2']
    option3 = request.form['Answer3']
    correct_option = request.form['correct_Answer']

    conn = sqlite3.connect('quizDatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (question_text, option1, option2, option3, correct_option)
        VALUES (?, ?, ?, ?, ?)
    ''', (question_text, option1, option2, option3, correct_option))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(debug=True)
