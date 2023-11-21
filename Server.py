import os
from flask import Flask, redirect, request,render_template
import json

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


if __name__ == "__main__":
    app.run(debug=True)
