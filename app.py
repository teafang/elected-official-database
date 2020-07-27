# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# load API key from .env
GOOGLE_CIVIC_API_KEY = os.getenv('GOOGLE_CIVIC_API_KEY')

# API endpoint
API_endpoint = 'https://www.googleapis.com/civicinfo/v2'



# -- Initialization section --
app = Flask(__name__)

address_to_officials = {
    '123 Chambers St':['Chuck Schumer','Kirsten Gillibrand','Bill de Blasio'],
    '456 Main St':['Kirsten Gillibrand','Chuck Schumer'],
}

senator_info = {
    'Chuck Schumer':{'name':'Chuck Schumer','office':'Senator'},
    'Kirsten Gillibrand':{'name':'Kirsten Gillibrand','office':'Senator'},
    'Bill de Blasio':{'name':'Bill de Blasio','office':'Mayor'},
}

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
  
@app.route('/results',methods=["POST","GET"])
def results():
    if request.method=="GET":
        return "you're getting the representative page"
    else:
        form = request.form
        address = form["address"]
        senator = address_to_officials[address]
        data={
            'senator':senator,
            'senator_info':senator_info,
        }
    return render_template("results.html", data=data)