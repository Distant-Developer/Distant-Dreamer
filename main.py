from flask import Flask, render_template
import mySQL

app = Flask(__name__)
db = mySQL.dataSQL("database.db")

@app.route('/')
def index():
    return render_template("mainPage.html")

@app.route("/lobby")
def lobby():
    return render_template("lobby.html")
    
if __name__ == "__main__":
    app.run()