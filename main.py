from flask import Flask, render_template, request
import mySQL
from secret import CLIENT_ID, CLIENT_SECRET
from routes.authentication import *

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.config["GITHUB_CLIENT_ID"] = CLIENT_ID
app.config["GITHUB_CLIENT_SECRET"] = CLIENT_SECRET

database = mySQL.dataSQL("database.db")

@app.route('/')
def index():
    return render_template("mainPage.html")

@app.route("/lobby")
def lobby():
    return render_template("lobby.html")

@app.route("/user", methods=['GET', 'POST'])
def userPage():
    if request.method == 'POST':
        incoming_message = request.form.get("description")  # Assuming you have a form field named 'message'
        print("Incoming message:", incoming_message)
        
    return render_template("userPage.html")

@app.route("/jobs")
def jobPostings():
    return render_template("jobPosting.html")

@app.route("/business") #this is for accessing a single business site 
def businessTemplate():
    return render_template("businessTemplate.html")

if __name__ == "__main__":
    app.register_blueprint(authentication)
    
    app.run()