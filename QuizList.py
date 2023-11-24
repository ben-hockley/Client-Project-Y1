import os

from flask import Flask, redirect, request, render_template

import sqlite3


DATABASE = 'QuizList.db'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)


@app.route("/Quizzes/AddDefualtQuiz", methods = ['GET'])

def quizAddDefaultDetails():

	try:
		conn = sqlite3.connect(DATABASE)
		cur = conn.cursor()

		cur.execute("INSERT INTO Quizzes ('quizName', 'genre', 'author')\
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


@app.route("/Quizzes/AddQuiz", methods = ['POST','GET'])

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
			cur.execute('INSERT INTO Quizzes(quizName, genre, author) VALUES (?, ?, ?)', (quizName, genre, author))
			conn.commit()

			msg = "Record successfully added"

		except:

			conn.rollback()
			msg = "error in insert operation"

		finally:
			conn.close()

			return msg



@app.route("/Quizzes/Search", methods = ['GET','POST'])

def quizSearch():

	if request.method =='GET':

		return render_template('QuizSearch.html')

	if request.method =='POST':

		try:

			quizName = request.form.get('quizName', default="Error") #rem: args for get form for post

			conn = sqlite3.connect(DATABASE)
			cur = conn.cursor()

			# accepts both list[] or tuple() list mutable tuple not-mutable

			cur.execute("SELECT * FROM Quizzes WHERE quizName=? ;", [quizName])

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

