from flask import Blueprint, current_app, jsonify, request, url_for, session, redirect, make_response
from authlib.integrations.flask_client import OAuth
from authlib.common.errors import AuthlibBaseError
from mySQL import database
from secret import *

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

    if not database.user_exists(profile["id"]): 
        database.use_database(
            "INSERT INTO users (token, username, email, github_url) VALUES (?, ?, ?, ?)",
            (
                profile["id"], 
                profile["login"],
                profile["email"],
                profile["html_url"]
            ),
        )
    
    id = database.use_database(
        "SELECT id FROM users WHERE token = ?",
        (profile["id"],)
    )[0]

    session["token"] =  str(profile["id"])
    session["username"] = str(profile["login"])

    session["id"] = id
    session["acct_type"] = "user" #user or business
    
    return redirect("lobby")


