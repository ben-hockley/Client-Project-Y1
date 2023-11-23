import os
from flask import Flask, redirect, request,render_template
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

@app.route("/accountDetails", methods=['GET'])
def returnAccountDetails():
    global user
    print(user)
    if request.method == 'GET':
        return render_template('Account_Details.html')

@app.route("/updateInfo", methods=['GET'])
def updateInfo():
    global User
    if user == None:
        return "None"
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute("\
        SELECT FirstName, SurName, Username FROM User WHERE Username = ?",([user]))
        details = cur.fetchall()
        newList = json.dumps(details[0])
        conn.close()
        return newList
    except Exception as e:
        conn.rollback()
        details = "None"
        print(e)
    conn.close()
    print(details)
    return details


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
        return message

@app.route("/usernameCheck")
def usernameCheck(username):
    """
    Function to check if the entered username exists within the database.
    Returns True if entered username doesn't exist, and False otherwise
    """
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute(\
        "SELECT Username FROM User WHERE Username = ?",([username]))
        isExist = cur.fetchall()
        cur.close()
        if isExist == []:
            return True
        else:
            return False
    except Exception as e:
        return False

# def usernameExistChecker(username):
#     """
#     Function to check if the entered username exists within the database.
#     Returns True if entered username doesn't exist, and False otherwise
#     """
#     try:
#         conn = sqlite3.connect('quizDatabase.db')
#         cur = conn.cursor()
#         cur.execute(\
#         "SELECT Username FROM User WHERE Username = ?",([username]))
#         isExist = cur.fetchall()
#         cur.close()
#         if isExist == []:
#             return True
#         else:
#             return False
#     except Exception as e:
#         return False

@app.route("/usernameExist", methods = ['POST'])
def usernameExist():
    if request.method == 'POST':
        firstName = request.form.get("firstName").title()
        lastName = request.form.get("lastName").title()
        userName = request.form.get("username")
        password = request.form.get("password")
        if usernameCheck(userName) == True:
            if submitNewAccount(firstName,lastName,userName,password) == True:
                message = "Welcome to your account, " + firstName
                global user
                user = userName
                return render_template('Account_Details.html', data = message)
            else:
                message = "Error inserting " + firstName
        else:
            message = "Username '" + userName + "' already exists."
        return render_template('Create_Account.html', data = message)



if __name__ == "__main__":
    app.run(debug=True)
