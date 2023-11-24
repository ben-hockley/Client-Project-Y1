import os
from flask import Flask, redirect, request,render_template
import json
import sqlite3

app = Flask(__name__)

user = None

def getQuestion(QuizID):
    data=[]
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute('SELECT Answer, question, QuizName, IsTrue, Questions.QuestionID FROM Answers, Questions, Quiz WHERE Answers.QuestionID = Questions.QuestionID AND Questions.QuizID = Quiz.QuizID AND Quiz.QuizID='+QuizID)
        data = cur.fetchall()
        conn.commit()
    except Exception as e:
        conn.rollback()
    questions=[]
    for i in data:
        questionID=""
        questionName=""
        trueAnswer=[]
        falseAnswer=[]
        quizName=""
        found = False
        for j in questions:
            if j[3] == i[4]:
                questionID=i[4]
                found = True
                break
        if found:
            for j in questions:
                if j[3]==questionID:
                    if i[3]=="T":
                        j[1].append(i[0])
                    else:
                        j[2].append(i[0])
        else:
            questionName=i[1]
            if i[3] == "T":
                trueAnswer.append(i[0])
            else:
                falseAnswer.append(i[0])
            question=(questionName, trueAnswer, falseAnswer, i[4], i[2])
            questions.append(question)
    return questions



@app.route("/userEnd", methods=['GET', 'POST'])
def userEnd():
    QuizID="50"
    UserID="21"
    if request.method == 'GET':
        return render_template('User End.html', data=getQuestion(QuizID))
    if request.method == 'POST':
        Points=4
        msg=""
        try:
            keys = request.form.keys()
            Points = []
            for i in keys:
                Points.append(i)
            print(Points)
            conn = sqlite3.connect('quizDatabase.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO Players(QuizID, UserID, Points) VALUES (?,?,?)', (QuizID, UserID, Points))
            data = cur.fetchall()
            conn.commit()
        except Exception as e:
            conn.rollback()
        return render_template('Main Page.html')

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



if __name__ == "__main__":
    app.run(debug=True)
