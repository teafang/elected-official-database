# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

### GOOGLE CIVIC API
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

### PROPUBLICA API (credits to Derek's API Review lab) ###
# load API key from .env
PROPUBLICA_API_KEY = os.getenv('PROPUBLICA_API_KEY')
# API endpoint
version = 'v1'
API_ENDPOINT = f'https://api.propublica.org/congress/{version}/'
API_AUTH = {'X-API-Key':PROPUBLICA_API_KEY}

## Sample API Request to get all of the members of the 116th House of Representatives
congress = 116
chamber = 'house'
API_URL = f"{API_ENDPOINT}/{congress}/{chamber}/members.json"
## The documentation for this API says to include the authentication key in the headers.
## To do that, we make a dictionary and use the headers keyword
r = requests.get(API_URL,headers=API_AUTH)
# We get the data from the request using .json()
propublica_data = r.json()
# Here, we're getting a list of members using the documentation
# WE need to access a dictionary, then a list, then another dictionary
# This gives us a list of all members of the house
# print(propublica_data['results'])
# members = propublica_data['results'][0]['members']
# for member in members:
#     for key in member:
#         print(f"{key}: {member[key]}")


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
        return "you're getting your elected officials page"
    else:
        form = request.form
        address = form["address"].replace(' ','%20')
        API_URL = f"{API_endpoint}/{API_request}?{API_query}={address}&key={GOOGLE_CIVIC_API_KEY}"
        # senator = address_to_officials[address]
        r = requests.get(API_URL)
        data_all=r.json()
        data={
            'offices':data_all.get('offices'),
            'officials':data_all.get('officials'),
        }
        if data['offices'] and data['officials']:
            print(data)
            print(API_URL)
            return render_template("results.html", data=data)
        else:
            data = {
                "error_message":"Invalid address, please try again in homepage."
            }
            return render_template("invalid_address.html",data=data)

@app.route('/propublica_api',methods=["POST","GET"])
def propublica():
    if request.method=="GET":
        return "you're getting the representative page"
    else:
        data = {}
        members = propublica_data['results'][0]['members']
        for member in members:
            for key in member:
                data[member['first_name']+member['last_name']+key] = member[key]
        print(data)
    return render_template("testing_propublica_api.html", data=data) ## change this to the real html file later
        # form = request.form
        # address = form["address"].replace(' ','%20')
        # API_URL = f"{API_endpoint}/{API_request}?{API_query}={address}&key={GOOGLE_CIVIC_API_KEY}"
        # # senator = address_to_officials[address]
        # r = requests.get(API_URL)
        # data_all=r.json()
        # data={
        #     'offices':data_all.get('offices'),
        #     'officials':data_all.get('officials'),
        # }
        # if data['offices'] and data['officials']:
        #     print(data)
        #     print(API_URL)
        #     return render_template("testing_propublica_api.html", data=data) ## change this to a different html file later
        # else:
        #     data = {
        #         "error_message":"Invalid address, please try again in homepage."
        #     }
        #     return render_template("invalid_address.html",data=data)