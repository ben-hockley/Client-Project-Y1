import os
from flask import Flask, redirect, request,render_template
import json

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)
