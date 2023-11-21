import os
from flask import Flask, redirect, request,render_template
import json

app = Flask(__name__)

@app.route("/createAccount", methods=['GET'])
def returnCreateAccount():
    if request.method == 'GET':
        return render_template('create Account.html')



if __name__ == "__main__":
    app.run(debug=True)
