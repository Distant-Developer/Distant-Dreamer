from functools import wraps
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
    return "id" in session

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not check_session(session=session):
            return redirect("/")
        return f(*args, **kwargs)
    return wrap

def verification_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if database.get_user(session["id"]).is_not_verified():
            return redirect("/verify")
        return f(*args, **kwargs)
    return wrap

def staff_only(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not database.get_user(session["id"]).is_staff:
            return redirect("/lobby")
        return f(*args, **kwargs)
    return wrap

@app.route('/')
def index():
    if check_session(session=session):
        return redirect("/lobby")
    
    return render_template("mainPage.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route("/lobby", methods=['GET','POST'])
@login_required
def lobby():
    
    if request.method != "POST":
        
        user = database.get_user(session["id"])
        
        return render_template("lobby.html", user=user, posts = database.get_all_posts()[::-1])
    
    if x := request.form.get("post_owner_id"):
        database.use_database(
            "INSERT INTO comments (owner_id, post_owner_id, content) VALUES (?, ?, ?)",
            (
                session["id"],
                x,
                request.form.get("content"),
            )
        )
    
    elif x := request.form.get("report"):
        database.use_database(
            "INSERT INTO reports (owner_id, reason, target_id, target_type) VALUES (?, ?, ?, ?)",
            (
                session["id"],
                x,
                request.form.get("id"),
                "post"
            )
        )

    return redirect("lobby")
    
    #sessionExists = check_session(session)


@app.route("/me", methods=['GET', 'POST'])
@login_required
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

        elif action == "addEdu": 
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
        
        elif x := request.form.get("linkedin_url"):
            database.use_database(
                "UPDATE users SET linkedin_url = ? WHERE id = ?", 
                (
                    x,
                    session["id"]
                )
            )

            database.use_database(
                "UPDATE users SET github_url = ? WHERE id = ?", 
                (
                    request.form.get("github_url"),
                    session["id"]
                )
            )

            database.use_database(
                "UPDATE users SET discord = ? WHERE id = ?", 
                (
                    request.form.get("discord"),
                    session["id"]
                )
            )
        
        elif x := request.form.get("username"):
            database.use_database(
                "UPDATE users SET username = ? WHERE id = ?", 
                (   
                    x,
                    session["id"]
                ),
            )
        elif x := request.form.get("logo_url"):
            database.use_database(
                "UPDATE users SET logo_url = ? WHERE id = ?", 
                (   
                    x,
                    session["id"]
                ),
            )

        
        return redirect(url_for('mePage'))

    user = database.get_user(session["id"])
        
    return render_template("me.html", experiences=user.experience, user=user, educations=user.education, badges = user.check_special_badges())

@app.route("/user")
@login_required
def userPage():
    try: targetuser = database.get_user(request.args.get("id"))
    except: return redirect("lobby")
    return render_template("user.html", user=database.get_user(session["id"]), experiences=targetuser.experience, targetuser=targetuser, educations=targetuser.education, badges=targetuser.check_special_badges())

@app.route("/jobs", methods=["POST","GET"])
@login_required
def jobPostings(priorityjob=None):
    if x := request.form.get("report"):
        database.use_database(
            "INSERT INTO reports (owner_id, reason, target_id, target_type) VALUES (?, ?, ?, ?)",
            (
                session["id"],
                x,
                request.form.get("id"),
                "jobPost"
            )
        )
        return redirect("/jobs")
    
    if id := request.args.get("id", None):
        priorityjob = database.get_jobpost(id=id)

    jobs = database.get_job_posts()

    try: return render_template("jobs.html", user= database.get_user(session["id"]), jobs=jobs, priorityjob = priorityjob)
    except: return redirect("/lobby")

@app.route("/verify", methods=['GET', 'POST'])
@login_required
def verify():

    user = database.get_user(session["id"])
    if user.is_verified: return redirect("lobby")
    
    if request.method == 'POST':
        if email := request.form.get("email"):

            if database.email_exist(email): return redirect("lobby")

            database.use_database(
                f"UPDATE users SET email = ? WHERE id = ?;", 
                (   
                    email,
                    session["id"]
                ),
            )
        
            SMTP.send_email(email, SMTP.generateCode(session["id"],email,request.user_agent.string))
            return redirect("verify")
            
        elif code := request.form.get("code"):
            #email already given
            id = SMTP.generateCode( session["id"] , user.email, request.user_agent.string)
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
@login_required
@verification_required
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
@login_required
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
@staff_only
@login_required
def staffPage():
    if x := request.form.get("exec"):
        database.use_database(
            x, (request.form.get("update"),)
        )

    

    user = database.get_user(session["id"])
    tables = database.get_tables()

    table = request.args.get("table", tables[0][0])


    column_names, data, count = database.get_all_data(table)

    return render_template("staff.html", user=user, tables=tables, table=table, column_names=column_names, data=[dict(zip(column_names, row)) for row in data], count=count, no_change={'token', 'id', 'type', 'email'})

@app.route("/staff/reports", methods=['GET','POST'])
@staff_only
@login_required
def staffReport():
    user = database.get_user(session["id"])

    reports = database.get_reports()

    if request.method != "POST":
        return render_template("staffReports.html", user=user, reports=reports[::-1])
    

    if (x := request.form.get("ignore", None)) or (x := request.form.get("shadow", None)):
        report_id = request.form.get("id")
        database.use_database(
            "UPDATE reports SET archived = 1, action = ?, action_reason = ? WHERE id = ?",
            ("ignored" if "ignore" in request.form else "unlisted", x, report_id)
        )

        if "shadow" in request.form: database.get_report(report_id).hide_content()


        

    return redirect("/staff/reports")


@app.route("/org/new", methods=['GET','POST'])
@login_required
@verification_required
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

        return redirect("/org/admin")
        

    user = database.get_user(session["id"])

    return render_template("createOrg.html", user=user)


@app.route("/org/list")
@login_required
@verification_required
def businessList():
    organizations = database.get_organizations()
    user = database.get_user(session["id"])

    return render_template("orgList.html", organizations=organizations[::-1], user=user)

@app.route("/org/admin", methods=['GET','POST'])
@login_required
@verification_required
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
    debug = True
    if not debug:
        from waitress import serve
        serve(app, host="0.0.0.0", port=PORT)
    else:
        app.run(host="0.0.0.0", port=PORT, debug=False, threaded=True)