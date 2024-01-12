import json
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

@app.route("/lobby", methods=['GET','POST'])
def lobby():
    
    if request.method == 'POST':
        database.use_database(
            "INSERT INTO comments (owner_id, post_owner_id, content) VALUES (?, ?, ?)",
            (
                session["id"],
                request.form.get("post_owner_id"),
                request.form.get("content"),
            )
        )

        return redirect("lobby")
    
    #sessionExists = check_session(session)

    user = database.get_user(session["id"])
    
    return render_template("lobby.html", user=user, posts = database.get_all_posts()[::-1])

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

    user = database.get_user(session["id"])

        
    return render_template("me.html", experiences=user.experience, user=user, educations=user.education)

@app.route("/user")
def userPage():
    id = request.args.get("id")
    targetuser = database.get_user(id)

    me = database.get_user(session["id"])

    return render_template("user.html", user=me, experiences=targetuser.experience, targetuser=targetuser, educations=targetuser.education)

@app.route("/jobs")
def jobPostings(priorityjob=None):
    #priorityJob means it will show up first. Can be used to see archived jobs
    
    if id := request.args.get("id", None):
        priorityjob = database.get_jobpost(id=id)

    jobs = database.get_job_posts()

    return render_template("jobs.html", user= database.get_user(session["id"]), jobs=jobs, priorityjob = priorityjob)

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


    return render_template("verify.html", user=user)


@app.route("/post/new", methods=['GET', 'POST'])
def createPost():
    if request.method == 'POST':
        action = request.form.get("action")

        if action == "Post":
            database.use_database(
                "INSERT INTO posts (owner_id, title, content) VALUES (?, ?, ?)",
                (
                    session["id"], 
                    request.form.get("title"),
                    request.form.get("content")
                ),
            )

            recentPost = database.get_post_by_user_id(session["id"])[-1]

            database.record_to_activity(recentPost.id, "posts")
            
            return redirect("/lobby")
        
    return render_template("createPost.html", title="", content="...", user=database.get_user(session["id"]))

@app.route("/post", methods=['GET', 'POST'])
def detailedPost():
    if request.method == 'POST':
        post_id = request.form.get("post_owner_id")
        database.use_database(
            "INSERT INTO comments (owner_id, post_owner_id, content) VALUES (?, ?, ?)",
            (
                session["id"],
                request.form.get("post_owner_id"),
                request.form.get("content"),
            )
        )

        return redirect("post?id="+post_id)

    user = database.get_user(session["id"])

    id = request.args.get("id", None)

    post = database.get_post_by_id(id=id)

    return render_template("detailedPost.html", post=post, user=user)
    

@app.route("/staff/sql", methods=['GET','POST'])
def staffPage():
    user = database.get_user(session["id"])
    if not user.is_staff: redirect("lobby") #Get him out!
    
    tables = database.get_tables()
    table = request.form.get("table", tables[0][0])
    column_names, data, count = database.get_all_data(table)
    return render_template("staff.html", user=user, tables=tables, column_names=column_names, data=data, count=count)

@app.route("/org/new", methods=['GET','POST'])
def createBusiness():
    if request.method == 'POST':
        name = request.form.get("name")
        tagline = request.form.get("tagline")
        website = request.form.get("website")
        industry = request.form.get("industry")
        size = request.form.get("size")
        logo = request.form.get("logo_url")


        database.use_database(
            "INSERT INTO organizations (owner_id, name, industry, tagline, website, size, logo_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                session["id"], 
                name,
                industry,
                tagline,
                website,
                size,
                logo
            ),
        )

        #database.record_to_activity(session["id"], "organizations")

        return redirect("/lobby")
        

    user = database.get_user(session["id"])

    return render_template("createOrg.html", user=user)


@app.route("/org/list")
def businessList():
    organizations = database.get_organizations()
    user = database.get_user(session["id"])

    return render_template("orgList.html", organizations=organizations, user=user)

@app.route("/org/admin", methods=['GET','POST'])
def org_Admin():
    user = database.get_user(session["id"])
    id = request.args.get("id", None)

    try: 
        org = database.get_organizations(id=id)[0]
        if org.owner_id == user.id:
            pass
        else:
            org = user.get_organizations()[0]
    except:
        org = user.get_organizations()[0]

    if request.method != 'POST':
        return render_template("adminOrg.html", user=user, org=org)
    
    if org_name := request.form.get("org_name"):
        org.updateName(org_name)
    elif newtagline := request.form.get("org_tagline"):
        org.updateDetails("tagline", newtagline)
    elif x := request.form.get("industry"):
        org.updateDetails("industry", x)
    elif x := request.form.get("size"):
        org.updateDetails("size", x)
    elif "postJobBoard" == request.form.get("action"):
        database.use_database(
            "INSERT INTO jobPost (owner_id, position_title, position_content, app_url) VALUES (?, ?, ?, ?)",
            (
                org.id,
                request.form.get("title"),
                request.form.get("content"),
                request.form.get("url"),
            ),
        )
    elif id := int(request.form.get("archive")):
        print(id)
        job = database.get_jobpost(id)
        job.archive()
    
    return redirect("/org/admin?id="+str(org.id))  


@app.route("/developer/job")
def jobDetails():
    id = request.args.get("id")
    job = database.get_jobpost(id)

    return {"ID":job.id, "OWNER_ID":job.owner_id, "POSITION_TITLE":job.position_title, "POSITION_CONTENT": job.position_content, "URL_APP":job.app_url, "ARCHIVED": job.archived}

@app.route("/developer/org")
def orgDetails():
    id = request.args.get("id")
    org = database.get_organizations(id=id)[0]

    return org.to_dict()


if __name__ == "__main__":

    app.register_blueprint(authentication)
    
    app.run()