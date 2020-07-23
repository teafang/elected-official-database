# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request


# -- Initialization section --
app = Flask(__name__)

address_to_officials = {
    '123 Chambers St':['Chuck Schumer','Kirsten Gillibrand'],
    '456 Main St':['Kirsten Gillibrand','Chuck Schumer'],
}

senator_info = {
    'Chuck Schumer':{'name':'Chuck Schumer','office':'Senator'},
    'Kirsten Gillibrand':{'name':'Kirsten Gillibrand','office':'Senator'},
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