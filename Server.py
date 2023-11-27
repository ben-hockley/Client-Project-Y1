import os
from flask import Flask, redirect, request,render_template
import json
import sqlite3

app = Flask(__name__)

ALLOWED_EXTENTIONS = set(['jpg', 'txt', 'svg', 'png', 'jpeg', 'gif'])

user = None

@app.route("/createAccount", methods=['GET'])
def returnCreateAccount():
    if request.method == 'GET':
        return render_template('Create_Account.html')

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



@app.route("/")
def redirectLogin():
    return redirect('/login')

@app.route("/login")
def returnLogin(): 
    return render_template('Log on.html')


@app.route("/loginFunction", methods=['POST'])
def logonFunction():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute(\
            "SELECT Password FROM User WHERE Username = ?",([username]))
            isExist = cur.fetchall()

            cur.close()
            if isExist != []:
                if isExist[0][0] == password:
                    global user
                    user = username
                    print('Signed in as', user)
                    return redirect("/home/" + user)
                else:
                    message = "Username and password don't match"
                    print(message)
                    return redirect('/login')
            else:
                message = "User not found"
                print(message)
                return redirect('/login')
        except Exception as e:
            cur.close()
            print(e)
            message = "Database error"
        print(message)
        return redirect('/login')

@app.route("/home/<user>")
def returnHome(user):
    try:
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute("SELECT FirstName, SurName FROM User WHERE Username = ?", (user,))
        account = cur.fetchone()
        cur.close()
        print('Welcome,', account[0], account[1] )

        if account:
            firstName, surname = account[0], account[1]
        else:
            firstName, surname = user, ""
            print('Error finding User')

        return render_template("Main Page.html", user=user, firstName=firstName, surname=surname)
    except Exception as e:
        print(e)
        print("Error accessing database")
        return redirect('/login')

@app.route("/accountDetails", methods=['GET'])
def returnAccountDetails():
    if request.method == 'GET':
        return render_template('Account_Details.html')
        
if __name__ == "__main__":
    app.run(debug=True)
