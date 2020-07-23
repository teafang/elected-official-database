# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request


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
        return "you're getting the representative page"
    else:
        form = request.form
        print(form)
        user_input = form["address"]
        data={
            user_input,
        }
        print(data)
    return render_template("results.html", data=data)