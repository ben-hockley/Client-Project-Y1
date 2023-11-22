import os
from flask import Flask, redirect, request,render_template
import json
import sqlite3

app = Flask(__name__)

user = None

@app.route("/login", methods=['GET'])
def returnLogin():
    if request.method == 'GET':
        return render_template('Log on.html')

@app.route("/logonFunction", methods=['POST'])
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
                    return render_template("Main Page.html")
                else:
                    message = "Username and password don't match"
            else:
                message = "User not found"
        except Exception as e:
            cur.close()
            print(e)
            message = "Database error"
        print(message)
        return redirect("/login")
        
if __name__ == "__main__":
    app.run(debug=True)
