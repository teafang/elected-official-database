# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import requests
import os
from dotenv import load_dotenv
load_dotenv()
import logging

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
# generating a list of all reps' names + their ProPublica ID
members = propublica_data['results'][0]['members']
members_id = {}
for member in members:
    if member['middle_name']==None:
        members_id[f"{member['first_name']} {member['last_name']}"] = member["id"]
    else:
        members_id[f"{member['first_name']} {member['middle_name'][0]}. {member['last_name']}"] = member["id"]

# -- Initialization section --
app = Flask(__name__)

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
  
@app.route('/results',methods=["POST","GET"])
def results():
    if request.method=="GET":
        return "You're getting your elected officials page"
    else:
        form = request.form
        address = form["address"].replace(' ','%20')
        # if len(address)==5:
            ## assume address is only a zipcode
            # API_URL = f"{API_endpoint}/{API_request}?{API_query}={address}&key={GOOGLE_CIVIC_API_KEY}"
        # else:
            ## assume address is a full address
        API_URL = f"{API_endpoint}/{API_request}?{API_query}={address}&key={GOOGLE_CIVIC_API_KEY}"
        r = requests.get(API_URL)
        data_all=r.json()
        print("Get to {0} return statuscode {1}".format(API_URL,r.status_code))
        data={
            'offices':data_all.get('offices'),
            'officials':data_all.get('officials'),
        }
        # print(data_all.get('offices'))
        if data['offices'] and data['officials']:
            # print(data)
            # print(API_URL)
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
        form = request.form
        data = {
            "name": form["name"],
        }
        # members = propublica_data['results'][0]['members']
        # for member in members:
        #     if member['middle_name']==None:
        #         data[f"{member['first_name']} {member['last_name']}"] = member["id"]
        #     else:
        #         data[f"{member['first_name']} {member['middle_name'][0]}. {member['last_name']}"] = member["id"]
        # print(data)
        if form.get("senator"):
            chamber = "senate"
            state = form["senator"][-2::]
            member_API_URL = f"https://api.propublica.org/congress/v1/members/{chamber}/{state}/current.json"
            r = requests.get(member_API_URL,headers=API_AUTH)
            member_id = r.json()["results"][0]["id"]
            votes_API_URL = f"https://api.propublica.org/congress/v1/members/{member_id}/votes.json"
            r = requests.get(votes_API_URL,headers=API_AUTH)
            data = r.json()['results'][0]['votes']
        elif form.get("representative"):
            chamber = "house"
            state = form["representative"][-8:-6:]
            district = form["representative"][-2::]
            member_API_URL = f"https://api.propublica.org/congress/v1/members/{chamber}/{state}/{district}/current.json"
            r = requests.get(member_API_URL,headers=API_AUTH)
            member_id = r.json()["results"][0]["id"]
            votes_API_URL = f"https://api.propublica.org/congress/v1/members/{member_id}/votes.json"
            r = requests.get(votes_API_URL,headers=API_AUTH)
            data = r.json()['results'][0]['votes']
        return render_template("testing_propublica_api.html", data=data) ## change this to the real html file later

@app.route('/about',methods=["GET"])
def about_page():
    return render_template("about.html")

@app.route('/resources',methods=["GET"])
def resources_page():
    return render_template("resources.html")