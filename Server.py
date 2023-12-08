import os
from flask import Flask, redirect, request, render_template, url_for
import json
import sqlite3
import hashlib
import random

app = Flask(__name__)

ALLOWED_EXTENTIONS = set(['jpg', 'txt', 'svg', 'png', 'jpeg', 'gif'])

user = None
UserID = 21
DATABASE = "quizDatabase.db"

@app.route("/createGuest")
def createGuest():
    conn = sqlite3.connect('quizDatabase.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM User')
    last = cur.fetchall()
    last = last[len(last)-1]
    conn.commit()
    conn.close()
    conn = sqlite3.connect('quizDatabase.db')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO User (Username, FirstName, SurName) VALUES ("{"Guest"+str(last[0]+1)}", "Guest", "{last[0]+1}")')
    conn.commit()
    conn.close()

    return redirect("/home/Guest"+str(last[0]+1))

@app.route("/checkGuest/<user>")
def checkGuest(user):
    conn = sqlite3.connect('quizDatabase.db')
    cur = conn.cursor()
    cur.execute(f'SELECT password FROM User WHERE Username = "{user}"')
    Password = cur.fetchone()[0]
    conn.commit()
    conn.close()
    if Password == None:
        return "T"
    return "F"

@app.route("/goHostEnd/<user>", methods=['POST'])
def goHostEnd(user):
    QuizKey = request.form.get("hostCode")
    print(QuizKey)
    return redirect(f"/hostEnd/{QuizKey}/{user}")

@app.route("/hostEnd/<QuizKey>/<user>")
def hostEnd(QuizKey, user):
    QuizName = request.form.get("QuizName")
    conn = sqlite3.connect("quizDatabase.db")
    cur = conn.cursor()
    cur.execute(f'SELECT QuizID FROM Quiz, User WHERE QuizKey = "{QuizKey}" AND Quiz.UserID = User.UserID')
    conn.commit()
    DATA = cur.fetchall()
    if DATA!=[]:
        cur.execute(f'SELECT Username, Points FROM Players, User WHERE User.UserID = Players.UserID AND Players.QuizID= "{DATA[0][0]}"')
        conn.commit()
        DATA = cur.fetchall()
        print(DATA)
    return render_template('Host End.html', data=DATA)

def RandomKey():
    while True:
        msg = ""
        Last_Quiz=""   
        CharList = []
        QuizKey = ""
        for i in range(65, 91):
            CharList.append(chr(i))
            CharList.append(chr(i + 32))
            for i in range(10):
                CharList.append(str(i))
        for i in range(4):
            QuizKey+=str(CharList[random.randint(0, len(CharList))])
        
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute(f'SELECT QuizName from Quiz where QuizKey = "{QuizKey}"')
        conn.commit()
        stuff = cur.fetchall()
        conn.close()
        print(stuff)
        if stuff == []:
            break
    return QuizKey

@app.route("/createQuiz/<user>", methods=['GET', 'POST'])
def createQuiz(user):
    if request.method == 'GET':
        return render_template('Create Quiz.html', QuizKey=RandomKey())
    if request.method =='POST':
        QuizName = request.form.get('QuizName')
        QuizKey = request.form.get('Key')
        print(QuizKey)
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute(f'SELECT UserID FROM User WHERE Username = "{user}"')
        conn.commit()
        ID = cur.fetchall()[0][0]
        conn.close()

        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute(f'SELECT QuizID FROM Quiz WHERE QuizName = "{QuizName}"')
        conn.commit()
        Exists = cur.fetchall()
        conn.close()

        if Exists == []:
            keys = request.form.keys()
            Elements = []
            for i in keys:
                Elements.append(i)
            Elements.remove("QuizName")
            Elements.remove("Key")
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

            try:
                conn = sqlite3.connect(DATABASE)
                cur = conn.cursor()
                cur.execute('INSERT INTO Quiz ("QuizName", "UserID", "QuizKey") VALUES (?, ?, ?)', (QuizName, ID, QuizKey))
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
            return redirect("/home/" + user)
        else:
            return render_template('Create Quiz.html',QuizKey=RandomKey() , data = "A quiz already has that name. Please try another.")

def getQuestion(QuizID):
    data=[]
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute('SELECT Answer, question, QuizName, IsTrue, Questions.QuestionID FROM Answers, Questions, Quiz WHERE Answers.QuestionID = Questions.QuestionID AND Questions.QuizID = Quiz.QuizID AND Quiz.QuizID = ?', [QuizID,])
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

def getMoodEmoji(mood):
    """
    Returns the code to display the mood on the page
    when the mood integer is passed as a parameter
    """
    moodlist = ["&#128549;","&#128577;","&#128528;","&#128578;","&#128512;"]
    return moodlist[mood]

def getMood(user):
    """
    Returns the integer which represents the user's mood within the database
    """
    try:
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute("SELECT Mood FROM User WHERE Username = ?", (user,))
        mood = cur.fetchone()[0]
    except Exception as e:
        conn.rollback()
        print(e)
        print("error retrieving mood")
        mood = None
    cur.close()
    return mood

@app.route("/moodChecker/<user>",methods=['GET','POST'])
def updateMood(user):
    """
    Function takes in the user's input from the slider and updates the database,
    before returning the home page
    """
    if request.method == 'GET':
        return render_template("moodChecker.html",user=user)
    if request.method == 'POST':
        mood = int(request.form.get("moodSlider"))
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("\
            UPDATE User SET Mood = ? WHERE Username = ?", (mood, user)\
            )
            conn.commit()
        except Exception as e:
            print(e)
            print("error during update")
            conn.rollback()
            return redirect("/moodChecker/" + user)
        conn.close()
        return redirect("/home/" + user)

@app.route("/moodBeforeSubmit/<user>", methods=['GET', 'POST'])
def moodBeforeSubmit(user):
    if request.method == 'POST':
        joinKey = request.form.get("joinCode")
        quizKeyExist = checkQuizKey(user, joinKey)
        if quizKeyExist == False:
            return redirect("/home/" + user)
        return redirect("/moodBefore/" + joinKey + "/" + user)

@app.route("/moodBefore/<joinKey>/<user>", methods=['GET', 'POST'])
def moodBefore(joinKey, user):
    if request.method == 'GET':
        return render_template('moodBefore.html', user=user, joinKey=joinKey)
    if request.method == 'POST':
        mood = int(request.form.get("moodSlider"))
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("\
            UPDATE User SET Mood = ? WHERE Username = ?", (mood, user)\
            )
            conn.commit()
        except Exception as e:
            print(e)
            print("error during update")
            conn.rollback()
            return redirect("/home/" + user)
        conn.close()
        return redirect("/joinQuizFunction/" + joinKey + "/" + user)

def getUserID(username):
    """
    Returns the userID of the username passed in as a parameter
    """
    try:
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute("\
        SELECT UserID FROM User WHERE Username = ?", (username,))
        userID = cur.fetchone()[0]
        conn.close()
        return userID
    except Exception as e:
        print(e)
        conn.close()
        return None

def getQuizID(user):
    """
    Returns the most recently played quiz's ID for the username given as a parameter
    Returns None if they haven't played any quizzes
    """
    userID = getUserID(user)
    try:
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute("\
        SELECT QuizID FROM Players WHERE UserID = ?", (userID,))
        quizID = cur.fetchall()
        conn.close()
        return quizID[-1][0]
    except Exception as e:
        print(e)
        conn.close()
        return None

@app.route("/moodAfter/<user>", methods=['GET', 'POST'])
def moodAfter(user):
    if request.method == 'GET':
        return render_template('moodAfter.html',user=user)
    if request.method == 'POST':
        moodAfter = int(request.form.get("moodSlider"))
        quizID = getQuizID(user)
        userID = getUserID(user)
        moodBefore = getMood(user)
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("\
            INSERT INTO Mood ('QuizID', 'UserID', 'MoodBefore', 'MoodAfter') VALUES (?,?,?,?)", \
            (quizID, userID, moodBefore, moodAfter))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        conn.close()
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("\
            UPDATE User SET Mood = ? WHERE Username = ?", (moodAfter, user)\
            )
            conn.commit()
        except Exception as e:
            print(e)
            print("error during update")
            conn.rollback()
            return redirect("/home/" + user)
        conn.close()
        return redirect("/home/" + user)

@app.route("/viewMoods/<user>", methods=['GET', 'POST'])
def viewMoods(user):
    if request.method == 'GET':
        return render_template("viewMoods.html")

@app.route("/updateQuizMood/<user>", methods=['GET', 'POST'])
def updateQuizMood(user):
    """
    Retrieves all the quiz names and moods from the database and returns them in a json list
    """
    if request.method == 'GET':
        userID = getUserID(user)
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("\
            SELECT Quizname, MoodBefore, MoodAfter FROM Mood\
            LEFT JOIN Quiz USING(QuizID)\
            WHERE Mood.UserID = ?", [userID,])
            bigList = cur.fetchall()
            conn.close()
            newDict = {}
            for x in range(len(bigList)):
                subList = []
                for y in range(len(bigList[x])):
                    subList.append(bigList[x][y])
                newDict.update({x: subList})
            jsonList = json.dumps(newDict)
            print(jsonList)
            return jsonList
        except Exception as e:
            print(e)
            conn.close()
            return None
        
@app.route("/userEnd/<QuizID>/<UserID>/<user>", methods=['GET', 'POST'])
def userEnd(QuizID, UserID, user):
    QuizID = int(QuizID)
    UserID = int(UserID)
    if request.method == 'GET':
        return render_template('User End.html', data=getQuestion(QuizID), QuizID = QuizID, UserID = UserID, user = user)
    if request.method == 'POST':
        Points = request.form.get("POINTS")
        msg=""
        try:
            conn = sqlite3.connect('quizDatabase.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO Players(QuizID, UserID, Points) VALUES (?,?,?)', (QuizID, UserID, Points))
            data = cur.fetchall()
            conn.commit()
        except Exception as e:
            conn.rollback()
        conn.close()
        return redirect("/moodAfter/" + user)

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
        SELECT FirstName, SurName, Username, Mood FROM User WHERE Username = ?",([user]))
        details = cur.fetchall()[0]
        firstname, surname, username, mood = details[0], details[1], details[2], details[3]
        details = [firstname, surname, username, getMoodEmoji(mood)]
        newList = json.dumps(details)
        conn.close()
        return newList
    except Exception as e:
        conn.rollback()
        details = "None"
        print(e)
    conn.close()
    print(details)
    return details

def submitNewAccount(firstName,lastName,userName,password,securityQuestion,securityAnswer):
    """
    Function to create a new entry in the User table.
    Takes all the data as parameters, and returns True if the insert was a success
    """
    try:
        conn = sqlite3.connect('quizDatabase.db')
        cur = conn.cursor()
        cur.execute(\
        "INSERT INTO User ('Username', 'FirstName','SurName','Password','Admin', 'SecurityQuestion', 'SecurityAnswer') \
        VALUES (?,?,?,?,?,?,?)", (userName,firstName,lastName,password,"N",securityQuestion,securityAnswer))
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
        firstName = request.form.get("firstName").title() #saves first letter as uppercase.
        lastName = request.form.get("lastName").title() #saves first letter as uppercase.
        userName = request.form.get("username")
        password = request.form.get("password")
        securityQuestion = request.form.get("securityQuestion")
        securityAnswer = request.form.get("securityAnswer")
        # Hashing password and security answer
        password = hashPassword(userName,password)
        securityAnswer = hashPassword(userName, securityAnswer)
        if usernameCheck(userName) == False:
            if submitNewAccount(firstName,lastName,userName,password,securityQuestion,securityAnswer) == True:
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

@app.route("/securityQuestionFunction", methods=['POST'])
def securityQuestionFunction():
    """
    Funtion that takes the inputs from Forgot Password form and checks to see if the user exists
    and that the security question + answer is correct for that user. If so then it redirects the user to
    the reset password page using their details.
    """
    if request.method == 'POST':
        user = request.form.get("username")
        securityQuestion = request.form.get("securityQuestion")
        securityAnswer = request.form.get("securityAnswer")
        securityAnswer = hashPassword(user, securityAnswer)
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute(\
            "SELECT securityQuestion,securityAnswer FROM User WHERE Username = ?",([user,]))
            isExist = cur.fetchall()
            cur.close()
            if isExist != []:
                if isExist[0][0] == securityQuestion and isExist[0][1] == securityAnswer:
                    return redirect("/resetPassword/" + user)
                else:
                    message = "Security Question/Answer are incorrect."
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

@app.route("/resetPassword/<user>", methods=['GET', 'POST'])
def resetPassword(user):
    if request.method == 'GET':
        return render_template("resetPassword.html", user=user)
    if request.method == 'POST':
        newPassword = request.form.get("password")
        newPassword = hashPassword(user, newPassword)
        try:
            conn = sqlite3.connect("quizDatabase.db")
            cur = conn.cursor()
            cur.execute("UPDATE User SET Password = ? WHERE Username = ?", (newPassword, user))
            conn.commit()
            conn.close()
            return redirect("/home/" + user)
        except Exception as e:
            print(e)
            conn.rollback()
            conn.close()
        return redirect("/")

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
        mood = getMood(user)
        mood = getMoodEmoji(mood)
        if account:
            firstName, surname = account[0], account[1]
        else:
            firstName, surname = user, ""
            print('Error finding User')

        return render_template("Main Page.html", user=user, firstName=firstName, surname=surname, mood=mood)
    except Exception as e:
        print(e)
        print("Error accessing database")
        return redirect('/login')

@app.route("/displayQuizzes/<user>", methods = ['GET', 'POST'])
def displayQuizzes(user):
    if request.method == 'GET':
        return render_template("ListQuizzes.html")

@app.route("/updateQuizDisplay", methods = ['GET'])
def updateQuizDisplay():
    """
    Function which fetches each quiz's name and unique code, returning them all in a json file
    """
    try:
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute("SELECT QuizName, QuizKey FROM Quiz")
        quizzes = cur.fetchall()
        newDict = {}
        i = 0
        for quiz in quizzes:
            newQuiz = [quiz[0], quiz[1]]
            newDict[i] = newQuiz
            i += 1
        newDict = json.dumps(newDict)
    except Exception as e:
        print(e)
        newDict = e
    conn.close()
    return newDict

def jls_extract_def():
    return 'quizName'

@app.route("/QuizHistory/<user>", methods = ['GET','POST'])
def quizSearch(user):
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
        QuizzesPlayed = str(len(QuizHistory))
        return render_template("Quiz History.html", user=user, QuizzesPlayed=QuizzesPlayed, QuizHistory=QuizHistory)
    except:
        print('there was an error')
    conn.close()
    return "error"
        
@app.route("/joinQuizFunction/<joinKey>/<user>", methods=['GET'])
def findQuizKey(joinKey, user):
    """
    Function that gets the Key from the input and checks to see if it relates to a Quiz Table
    """
    if request.method == 'GET':
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
                # return redirect('userEnd/' + user, QuizID=QuizID, UserID=UserID)
                return redirect('/userEnd/' + str(QuizID) + '/' + str(UserID) + '/' + user)

            else:
                errormessage = "Quiz not found"
                print(errormessage)
                return redirect('/home/' + user)

        except Exception as e:
            print(e)
            print("Error accessing Database")
            return redirect('/')

def checkQuizKey(user, joinKey):

    try:
        conn = sqlite3.connect("quizDatabase.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Quiz WHERE QuizKey = ?",(joinKey,))
        conn.commit()
        Quiz = cur.fetchall()
        QuizID = Quiz[0][0]
        conn.close()
        if QuizID:
            return True
        else:
            errormessage = "Quiz not found"
            print(errormessage)
            return False
    except Exception as e:
        conn.close()
        print(e)
        return False
@app.route("/forgotPassword")
def forgotPassword():
    return render_template("forgotPassword.html")

if __name__ == "__main__":
    app.run(debug=True)