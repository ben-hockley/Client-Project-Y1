import os
from flask import Flask, redirect, request,render_template
import json
import sqlite3

app = Flask(__name__)


@app.route("/createAccount", methods=['GET'])
def returnCreateAccount():
    if request.method == 'GET':
        return render_template('Create Account.html')

@app.route("/mainPage", methods=['GET'])
def returnHome():
    if request.method == 'GET':
        return render_template('Main Page.html')

@app.route("/submitNewAccount", methods=['POST'])
def submitNewAccount():
    if request.method == 'POST':
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        userName = request.form.get("username")
        password = request.form.get("password")
        try:
            conn = sqlite3.connect('Quiz.db')
            cur = conn.cursor()
            cur.execute(\
            "INSERT INTO User ('Username', 'FirstName','SurName','Password','Admin') \
            VALUES (?,?,?,?,?)", (userName,firstName,lastName,password,"N"))
            print("Successfully inserted " + firstName)
        except Exception as e:
            conn.rollback()
            print("Error during insert")
            print(e)
        finally:
            conn.commit()
            conn.close()
            return render_template('Main Page.html')

# @app.route("/usernameExist", methods = ['POST'])
# def usernameExist():
#     if request.method == 'POST':
#         firstName = request.form.get("firstName")
#         lastName = request.form.get("lastName")
#         userName = request.form.get("username")
#         password = request.form.get("password")
#         conn = sqlite3.connect('Quiz.db')
#         cur = conn.cursor()
#         isExist = cur.execute(\
        
#         )



if __name__ == "__main__":
    app.run(debug=True)
