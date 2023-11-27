import os
from flask import Flask, redirect, request,render_template
import json
import sqlite3
import hashlib

app = Flask(__name__)

ALLOWED_EXTENTIONS = set(['jpg', 'txt', 'svg', 'png', 'jpeg', 'gif'])

user = None
DATABASE = "quizDatabase.db"

@app.route("/createQuiz", methods=['GET', 'POST'])
def returnFirst():
    if request.method == 'GET':
        return render_template('Create Quiz.html')
    if request.method =='POST':
        QuizName = request.form.get('QuizName')
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute(f'SELECT QuizID FROM Quiz WHERE QuizName = "{QuizName}"')
        conn.commit()
        Exists = cur.fetchall()
        conn.close()
        if Exists == []:
            keys = request.form.keys()
            print(keys)
            Elements = []
            for i in keys:
                Elements.append(i)
            Elements.remove("QuizName")
            Numbers = []
            for i in Elements:
                IsIn = False
                for j in Numbers:
                    if i[0]==j:
                        IsIn=True
                        break
                if IsIn==False:
                    Numbers.append(i[0])
            Identity = []
            Quiz = []
            for i in Numbers:
                for j  in Elements:
                    if j[0] == i:
                        Identity.append(j)
                Quiz.append(Identity)
                Identity= []
            points = 0
            for i in Quiz:
                points+=1
            msg = ""
            Last_Quiz=""   
            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute('INSERT INTO Quiz ("QuizName", "UserID") VALUES (?, ?)', (QuizName, "21"))
                conn.commit()
                Last_Quiz = cur.lastrowid
                conn.close()
            except Exception as e:
                conn.rollback()
            for question in Quiz:
                questionName = request.form.get(question[0])
                question.remove(question[0])
                Last_Question=""
                try:
                    conn = sqlite3.connect(DATABASE)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Questions ("Question", "QuizID", Points) VALUES (?, ?, ?)', (questionName, Last_Quiz, points))
                    conn.commit()
                    Last_Question = cur.lastrowid
                    conn.close()
                except Exception as e:
                    conn.rollback()
                for i in range(len(question)):
                    answerName=request.form.get(question[i-1])
                    if (question[i-1])[-3:-1] != "Is":
                        questionay = (question[i])
                        if questionay[-3:-1] == "Is":
                            try:
                                conn = sqlite3.connect(DATABASE)
                                cur = conn.cursor()
                                cur.execute('INSERT INTO Answers ("Answer", "QuestionID", "IsTrue") VALUES (?, ?, ?)', (answerName, Last_Question, "T"))
                                conn.commit()
                                conn.close()
                            except Exception as e:
                                conn.rollback()
                        else:
                            try:
                                conn = sqlite3.connect(DATABASE)
                                cur = conn.cursor()
                                cur.execute('INSERT INTO Answers ("Answer", "QuestionID", "IsTrue") VALUES (?, ?, ?)', (answerName, Last_Question, "F"))
                                conn.commit()
                                conn.close()
                            except Exception as e:
                                conn.rollback()
            return render_template('Main Page.html')
        else:
            return render_template('Create Quiz.html', data = "A quiz already has that name. Please try another.")


@app.route("/createAccount", methods=['GET'])
def returnCreateAccount():
    if request.method == 'GET':
        return render_template('Create_Account.html')

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

def hashPassword(username, password):
    """
    Function which receives username and password as a parameter and returns a hash of password
    """
    # Hashing the password, adding the username as salt
    # https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/
    database_password = password + username
    hashed = hashlib.md5(database_password.encode())
    password = hashed.hexdigest()
    return password

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
        # Hashing password
        password = hashPassword(userName,password)
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
        # Hashing password
        password = hashPassword(username, password)
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
