import os
from flask import Flask, redirect, request,render_template
import json

app = Flask(__name__)

@app.route("/Log on", methods=['GET'])
def returnSecond():
    if request.method == 'GET':
        return render_template('Log on.html')
        
if __name__ == "__main__":
    app.run(debug=True)
