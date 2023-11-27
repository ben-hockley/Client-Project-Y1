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

#taken this out as alternative was made for testing different route with better naming

# @app.route("/mainPage", methods=['GET'])
# def returnHome():
#     if request.method == 'GET':
#         return render_template('Main_Page.html')

@app.route("/accountDetails", methods=['GET'])
def returnAccountDetails():
    if request.method == 'GET':
        return render_template('Account_Details.html')

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
                    print(user)
                    return redirect("/home")
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

@app.route("/home")
def returnHome():
        return render_template("Main Page.html")
        
DATABASE = 'QuizList.db'

@app.route("/QuizHistory/AddDefualtQuiz", methods = ['GET'])

def quizAddDefaultDetails():

	try:
		conn = sqlite3.connect(DATABASE)
		cur = conn.cursor()

		cur.execute("INSERT INTO QuizHistory ('quizName', 'genre', 'author')\
					 VALUES (?,?,?)",("General Knowledge", "Social", "Ben") )
		conn.commit()

		msg = "Record successfully added"

	except:

		conn.rollback()

		msg = "error in insert operation"

	finally:
		conn.close()

		return msg


def jls_extract_def():
    return 'quizName'


@app.route("/QuizHistory/AddQuiz", methods = ['POST','GET'])

def quizAddDetails():

	if request.method =='GET':

		return render_template('QuizData.html')

	if request.method =='POST':

		quizName = request.form.get(jls_extract_def(), default="Error")#rem: args for get form for post
		genre = request.form.get('genre', default="Error")
		author = request.form.get('author', default="Error")
		print("inserting quiz"+quizName)

		try:
			conn = sqlite3.connect(DATABASE)
			cur = conn.cursor()
			cur.execute('INSERT INTO QuizHistory(quizName, genre, author) VALUES (?, ?, ?)', (quizName, genre, author))
			conn.commit()

			msg = "Record successfully added"

		except:

			conn.rollback()
			msg = "error in insert operation"

		finally:
			conn.close()

			return msg



@app.route("/QuizHistory/Search", methods = ['GET','POST'])

def quizSearch():

	if request.method =='GET':

		return render_template('QuizSearch.html')

	if request.method =='POST':

		try:

			quizName = request.form.get('quizName', default="Error") #rem: args for get form for post

			conn = sqlite3.connect(DATABASE)
			cur = conn.cursor()

			# accepts both list[] or tuple() list mutable tuple not-mutable

			cur.execute("SELECT * FROM QuizHistory WHERE quizName=? ;", [quizName])

			data = cur.fetchall()
			print(data)
			print(data)
		except:

			print('there was an error', data)
			conn.close()

		finally:
			conn.close()
			return str(data)

			# return render_template('ListStudents.html', data = data)



if __name__ == "__main__":

	app.run(debug=True)

	#app.run(host='0.0.0.0', port=8080)

