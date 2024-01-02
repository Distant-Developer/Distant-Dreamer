from flask import Flask, render_template, request
import mySQL

app = Flask(__name__)
db = mySQL.dataSQL("database.db")

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

if __name__ == "__main__":
    app.run()