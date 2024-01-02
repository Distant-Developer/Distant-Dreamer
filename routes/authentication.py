from flask import Blueprint, current_app, request, url_for, session, redirect, make_response
from authlib.integrations.flask_client import OAuth
from authlib.common.errors import AuthlibBaseError
from mySQL import dataSQL
from secret import *
from main import database
from discord import *

authentication = Blueprint("authentication", __name__)
oauth = OAuth(current_app)
GITHUB = oauth.register(
    name="github",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    scope="read:user,user:email"
)

@authentication.route("/login")
def login():
    return GITHUB.authorize_redirect(GIT_OAUTH_CALLBACK_URL)


@authentication.route("/authorize")
def authorize():
    resp = oauth.create_client("github").get(
        "user", token=GITHUB.authorize_access_token()
    )
    profile = resp.json()
    print(profile.get('email'))

    x = database.execute_script(
        "SELECT COUNT(*) FROM users WHERE token = ?", (profile["id"],)
    )
    if int(x[0]) >= 1:  # check if acct with token already exists
        session["id"] = profile["id"]

        session["id"] =  str(profile["id"])
        session["username"] = str(profile["login"])
        target = session["id"]
        return redirect("lobby")

    db_thread = Thread(target=dataSQL(dbfile="database.db").use_database, args=(
        "INSERT INTO users (username, token) VALUES (?, ?)",
        (
            profile["login"],
            profile["id"],
        ),
    )
    )
    db_thread.start()
    session["id"] = profile["id"]
    session["id"] =  str(profile["id"])
    session["username"] = str(profile["login"])

    
    return redirect("lobby")