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
    """
    Function fetches all the user data from the database, returns it in a JSON list
    If not found, returns None
    """
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
    """
    Function to create a new entry in the User table.
    Takes all the data as parameters, and returns True if the insert was a success
    """
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
    Returns True if entered username does exist, and False otherwise
    """
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute(\
        "SELECT Username FROM User WHERE Username = ?",([username]))
        isExist = cur.fetchall()
        conn.close()
        if isExist == []:
            return False
        else:
            return True
    except Exception as e:
        conn.close()
        return e


@app.route("/usernameExist", methods = ['POST'])
def usernameExist():
    """
    Route which gets the form submission from the HTML page,
    checks if the username exists already, and inserts the information to the database if not
    Returns either the Account_Details.html page if successful, or Create_Account.html if unsuccessful
    """
    if request.method == 'POST':
        firstName = request.form.get("firstName").title()
        lastName = request.form.get("lastName").title()
        userName = request.form.get("username")
        password = request.form.get("password")
        if usernameCheck(userName) == False:
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

@app.route("/updateUsername", methods=['POST'])
def updateUsername():
    """
    Function which will update the new username entered by a user
    """
    if request.method == 'POST':
        global user
        username = request.form.get("newUsername")
        if username == '':
            return render_template("Account_Details.html")
        if usernameCheck(username) == False:
            try:
                conn = sqlite3.connect('quizDatabase.db')
                cur = conn.cursor()
                cur.execute(\
                "UPDATE User SET ('Username') = ? WHERE Username = ?", (username,user))
                conn.commit()
                message = "Successfully updated username"
                user = username
            except Exception as e:
                print(e)
                message = "Error during update"
                conn.rollback()
            finally:
                print(message)
                conn.close()
        else:
            message = "New username '" + username + "' already exists."
        return render_template("Account_Details.html", data = message)

@app.route("/updateFirstname", methods=['POST'])
def updateFirstname():
    """
    Function which will update the new first name entered by a user
    """
    if request.method == 'POST':
        global user
        firstname = request.form.get("newFirstname").title()
        if firstname == '':
            return render_template("Account_Details.html")
        try:
            conn = sqlite3.connect('quizDatabase.db')
            cur = conn.cursor()
            cur.execute(\
            "UPDATE User SET ('FirstName') = ? WHERE Username = ?", (firstname,user))
            conn.commit()
            message = "Successfully updated first name"
        except Exception as e:
            print(e)
            message = "Error during update"
            conn.rollback()
        finally:
            print(message)
            conn.close()
        return render_template("Account_Details.html", data = message)
                
@app.route("/updateLastname", methods=['POST'])
def updateLastname():
    """
    Function which will update the new last name entered by a user
    """
    if request.method == 'POST':
        global user
        lastname = request.form.get("newLastname").title()
        if lastname == '':
            return render_template("Account_Details.html")
        try:
            conn = sqlite3.connect('quizDatabase.db')
            cur = conn.cursor()
            cur.execute(\
            "UPDATE User SET ('SurName') = ? WHERE Username = ?", (lastname,user))
            conn.commit()
            message = "Successfully updated last name"
        except Exception as e:
            print(e)
            message = "Error during update"
            conn.rollback()
        finally:
            print(message)
            conn.close()
        return render_template("Account_Details.html", data = message)




if __name__ == "__main__":
    app.run(debug=True)
