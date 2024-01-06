import re
from flask import Flask, render_template, request
from mySQL import database
from secret import CLIENT_ID, CLIENT_SECRET
from routes.authentication import *
import SMTP

app = Flask(__name__,static_folder='static')
app.secret_key = "SECRET_KEY"
app.config["GITHUB_CLIENT_ID"] = CLIENT_ID
app.config["GITHUB_CLIENT_SECRET"] = CLIENT_SECRET



def check_session(session):
    return "token" in session and "username" in session and "id" in session

import markdown

def convert_markdown_to_html(raw_text):
    if raw_text == "" or raw_text == None:
        return
    # Define the pattern for matching <script> ... </script>
    script_pattern = re.compile(r'<script\b[^>]*>.*?</script>', re.DOTALL)

    # Use sub() method to replace matched patterns with an empty string
    result_string = re.sub(script_pattern, '', raw_text)

    html_content = markdown.markdown(raw_text)
    return html_content



@app.route('/')
def index():
    return render_template("mainPage.html")

@app.route("/lobby")
def lobby():
    sessionExists = check_session(session)

    print(session["client"])

    user = database.get_user(session["client"]["id"])
    bussinessAccounts = database.get_organizations(id=None, owner_id=session["id"])

    return render_template("lobby.html", session=user, bussinessAccounts=bussinessAccounts)

@app.route("/me", methods=['GET', 'POST'])
def mePage():
    if request.method == 'POST':
        action = request.form.get("action")  # Assuming you have a form field named 'message'
        if action == "addExp": 
            database.use_database(
                "INSERT INTO experiences (associated_user_id, company_name, company_logo_url, position_title, position_description, dates) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    session["id"], 
                    request.form.get("company_name"),
                    request.form.get("company_logo"),
                    request.form.get("position_name"),
                    request.form.get("description"),
                    request.form.get("position_dates")
                    
                ),
            )

            pass
        elif action == "editExp":
            database.use_database(
                f"UPDATE experiences SET company_name = ?, company_logo_url = ?, position_title = ?, position_description = ?, dates = ? WHERE id = ?;", 
                (   
                    request.form.get("company_name"),
                    request.form.get("company_logo"),
                    request.form.get("position_name"),
                    request.form.get("description"),
                    request.form.get("position_dates"),
                    request.form.get("unique_id")
                ),
            )
        
        elif action == "delExp":
            database.use_database(
                "DELETE FROM experiences WHERE id = ?", 
                (   
                    request.form.get("unique_id")
                ),
            )

        if action == "addEdu": 
            database.use_database(
                "INSERT INTO educations (associated_user_id, tuition_name, tuition_logo_url, position_description, dates) VALUES (?, ?, ?, ?, ?)",
                (
                    session["id"], 
                    request.form.get("campus_name"),
                    request.form.get("campus_logo"),
                    request.form.get("description"),
                    request.form.get("dates")
                    
                ),
            )

        elif action == "editEdu":
            database.use_database(
                f"UPDATE educations SET tuition_name = ?, tuition_logo_url = ?, position_description = ?, dates = ? WHERE id = ?;", 
                (   
                    request.form.get("campus_name"),
                    request.form.get("campus_logo"),
                    request.form.get("description"),
                    request.form.get("dates"),
                    request.form.get("unique_id")
                ),
            )
        
        elif action == "delEdu":
            database.use_database(
                "DELETE FROM educations WHERE id = ?", 
                (   
                    request.form.get("unique_id")
                ),
            )
        
        elif action == "upDescription":
            database.use_database(
                "UPDATE users SET description = ? WHERE id = ?", 
                (   
                    request.form.get("description"),
                    session["id"]
                ),
            )

        
        return redirect(url_for('mePage'))

            
    experiences = database.get_experiences(session["id"])
    educations = database.get_educations(session["id"])
    user = database.get_user(session["id"])

        
    return render_template("me.html", experiences=experiences, user=user, educations=educations)

@app.route("/user")
def userPage():
    id = request.args.get("id")
    experiences = database.get_experiences(id)
    educations = database.get_educations(id)
    user = database.get_user(id)

    return render_template("user.html", experiences=experiences, user=user, educations=educations)


@app.route("/jobs")
def jobPostings():
    return render_template("jobs.html")

@app.route("/business") #this is for accessing a single business site 
def businessTemplate():
    return render_template("businessTemplate.html")

@app.route("/verify", methods=['GET', 'POST'])
def verify():
    user = database.get_user(session["id"])

    if request.method == 'POST':
        if email := request.form.get("email"):

            if user.is_verified: #if email already verified...then no need to change it.
                return redirect("lobby")


            database.use_database(
                f"UPDATE users SET email = ? WHERE id = ?;", 
                (   
                    email,
                    session["id"]
                ),
            )
        
            SMTP.send_email(email, SMTP.generateCode(session["id"],email))

            return redirect("verify")
            
        elif code := request.form.get("code"):
            #email already given
            id = SMTP.generateCode( str(session["id"]) , user.email)
            if id == code:
                database.use_database(
                    f"UPDATE users SET is_verified = ? WHERE id = ?;", 
                    (   
                        1,
                        session["id"]
                    ),
                )

                return redirect("lobby")


    return render_template("verify.html")


@app.route("/post/create", methods=['GET', 'POST'])
def createPost():
    if request.method == 'POST':
        action = request.form.get("action")
        print(action)
        if action == "Preview":
            return render_template("createPost.html", title=request.form.get("title", None), bef_content=request.form.get("content", None), content=convert_markdown_to_html(request.form.get("content", None)), user=database.get_user(session["id"]))
    
        elif action == "Post":
            database.use_database(
                "INSERT INTO posts (owner_id, title, content) VALUES (?, ?, ?)",
                (
                    session["id"], 
                    request.form.get("title"),
                    request.form.get("content")
                ),
            )

            database.record_to_activity(session["id"], "posts")
            
            return redirect("lobby")
        
    return render_template("createPost.html", title="", content="...", user=database.get_user(session["id"]))

@app.route("/staff", methods=['GET','POST'])
def staffPage():
    tables = database.get_tables()

    table = request.form.get("table", tables[0][0])


    column_names, data, count = database.get_all_data(table)
    
    return render_template("staffPage.html", tables=tables, column_names=column_names, data=data, count=count)

@app.route("/org/new", methods=['GET','POST'])
def createBusiness():
    if request.method == 'POST':
        name = request.form.get("name")
        tagline = request.form.get("tagline")
        website = request.form.get("website")
        industry = request.form.get("industry")
        size = request.form.get("size")


        database.use_database(
            "INSERT INTO organizations (owner_id, name, industry, tagline, website, size, logo_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                session["id"], 
                name,
                industry,
                tagline,
                website,
                size,
                "https://raw.githubusercontent.com/Distant-Developer/Distant-Dreamer/df49365f163fa4b1e9ffd9f68678fecf8ad0efcf/static/img/defaultImage.svg"
            ),
        )

        return redirect("lobby")
        

    return render_template("createOrg.html")


@app.route("/org/list")
def businessList():
    organizations = database.get_organizations()

    return render_template("businessList.html", organizations=organizations)

if __name__ == "__main__":

    app.register_blueprint(authentication)
    
    app.run()