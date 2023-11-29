import os
from flask import Flask, redirect, request, render_template, url_for
import json
import sqlite3
import hashlib

app = Flask(__name__)

ALLOWED_EXTENTIONS = set(['jpg', 'txt', 'svg', 'png', 'jpeg', 'gif'])

user = None
UserID = 21
DATABASE = "quizDatabase.db"

@app.route("/hostEnd", methods=['GET','POST'])
def hostEnd():
    if request.method =='GET':
        return render_template('Host End.html', data=[])
    if request.method =='POST':
        QuizName = request.form.get("QuizName")
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute(f'SELECT QuizID FROM Quiz, User WHERE QuizName = "{QuizName}" AND Quiz.UserID = User.UserID AND User.Admin = "Y"')
        conn.commit()
        DATA = cur.fetchall()

        if DATA!=[]:
            cur.execute(f'SELECT Username, Points FROM Players, User WHERE User.UserID = Players.UserID AND Players.QuizID= "{DATA[0][0]}"')
            conn.commit()
            DATA = cur.fetchall()
            print(DATA)
        return render_template('Host End.html', data=DATA)

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
    QuizID = request.args.get('QuizID')
    UserID = request.args.get('UserID')
    # if request.method == 'GET':
    return render_template('User End.html', data=getQuestion(QuizID))
    if request.method == 'POST':
        Points = request.form.get("POINTS")
        print(Points)
        msg=""
        try:
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

@app.route("/accountDetails/<user>", methods=['GET'])
def returnAccountDetails(user):
    if request.method == 'GET':
        return render_template('Account_Details.html')


@app.route("/updateInfo/<user>", methods=['GET'])
def updateInfo(user):
    """
    Function fetches all the user data from the database, returns it in a JSON list
    If not found, returns None
    """
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
                user = userName
                return redirect("/accountDetails/" + user)
            else:
                message = "Error inserting " + firstName
        else:
            message = "Username '" + userName + "' already exists."
        return redirect("/createAccount")

@app.route("/updateUsername/<user>", methods=['POST'])
def updateUsername(user):
    """
    Function which will update the new username entered by a user
    """
    if request.method == 'POST':
        username = request.form.get("newUsername")
        if username == '':
            return redirect("/accountDetails/" + user)
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
        return redirect("/accountDetails/" + user)

@app.route("/updateFirstname/<user>", methods=['POST'])
def updateFirstname(user):
    """
    Function which will update the new first name entered by a user
    """
    if request.method == 'POST':
        firstname = request.form.get("newFirstname").title()
        if firstname == '':
            return redirect("/accountDetails/" + user)
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
        return redirect("/accountDetails/" + user)
                
@app.route("/updateLastname/<user>", methods=['POST'])
def updateLastname(user):
    """
    Function which will update the new last name entered by a user
    """
    if request.method == 'POST':
        lastname = request.form.get("newLastname").title()
        if lastname == '':
            return redirect("/accountDetails/" + user)
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
        return redirect("/accountDetails/" + user)

@app.route("/")
def redirectLogin():
    return redirect('/login')

@app.route("/login")
def returnLogin(): 
    return render_template('Log on.html')

@app.route("/loginFunction", methods=['POST'])
def logonFunction():
    """
    Funtion that takes the inputs from Log in form and checks to see if the user exists
    and that the password is correct for that user. If so then it redirects the user to
    the homepage using their details.
    """
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
    """
    Function to load the home page using details passed through from the login function.
    User is passed through to source the details from the database and use within the HTML. 
    """
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

QUIZLISTDATABASE = 'quizDatabase.db'

@app.route("/listQuizzes")
def printQuiz():
    return render_template("ListQuizzes.html")


def jls_extract_def():
    return 'quizName'




@app.route("/QuizHistory/<user>", methods = ['GET','POST'])

def quizSearch(user):
    if request.method =='GET':
        return render_template('QuizSearch.html',user=user)
    if request.method =='POST':
        try:
            quizName = request.form.get('QuizName', default="Error") #rem: args for get form for post
            conn = sqlite3.connect(QUIZLISTDATABASE)
            cur = conn.cursor()
            print(user)
            cur.execute("SELECT UserID FROM User WHERE Username = ?", (user,))
            userID = cur.fetchone()[0]
            print(userID)
            cur.execute("SELECT QuizName FROM Quiz WHERE UserID = ?", (userID,))
            QuizHistory = cur.fetchall()
            quiz_history = json.dumps(QuizHistory)
            QuizzesPlayed = str(len(QuizHistory))
            return render_template("Quiz History.html", user=user, QuizzesPlayed=QuizzesPlayed, QuizHistory=QuizHistory),quiz_history
        except:
            print('there was an error')
        conn.close()
        return "error"
        
@app.route("/joinQuizFunction", methods=['POST'])
def findQuizKey():
    """
    Function that gets the Key from the input and checks to see if it relates to a Quiz Table
    """
    if request.method == 'POST':
        #Take the Input from the form
        joinKey = request.form.get("joinCode")
        print(joinKey)

        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM Quiz WHERE QuizKey = ?",(joinKey,))
            conn.commit()
            Quiz = cur.fetchall()
            cur.execute("SELECT * FROM User WHERE UserName = ?",(user,))
            conn.commit()
            User = cur.fetchall()
            cur.close()
            
            QuizID = Quiz[0][0]
            QuizName = Quiz[0][1]
            UserID = User[0][0]
            print(QuizID)
            print(QuizName)
            print(UserID)
            
            if QuizID:
                return redirect(url_for('userEnd', QuizID=QuizID, UserID=UserID))

            else:
                errormessage = "Quiz not found"
                print(errormessage)
                return redirect('/')

        except Exception as e:
            print(e)
            print("Error accessing Database")
            return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

