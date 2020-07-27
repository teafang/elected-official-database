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

# API request to get `representative by address` dictionary
API_request = 'representatives'
API_query = 'address'
# address='345%20Chambers%20St,%20New%20York,%20NY%2010282'
address=''
def change_address(new_address):
    return new_address.replace(' ','%20')
address = change_address('41 Seaver Way, Queens, NY 11368')
API_URL = f"{API_endpoint}/{API_request}?{API_query}={address}&key={GOOGLE_CIVIC_API_KEY}"
# print(API_URL)

## https://www.googleapis.com/civicinfo/v2/representatives?address=345%20Chambers%20St,%20New%20York,%20NY%2010282&key=AIzaSyDUXNPT5bEGS1fn3eTdOaqFQW8gHHftozY



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
        address = form["address"].replace(' ','%20')
        API_URL = f"{API_endpoint}/{API_request}?{API_query}={address}&key={GOOGLE_CIVIC_API_KEY}"
        # senator = address_to_officials[address]
        r = requests.get(API_URL)
        data_all=r.json()
        data={
            'offices':data_all['offices'],
            'officials':data_all['officials'],
        }
        print(data)
        print(API_URL)
    return render_template("results.html", data=data)