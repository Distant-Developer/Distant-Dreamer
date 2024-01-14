from flask import Blueprint, abort, current_app, jsonify, request, url_for, session, redirect, make_response
from authlib.integrations.flask_client import OAuth
import google_auth_oauthlib
import requests
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
    git_token = str(profile["id"])

    if not database.user_exists(profile["id"]): 
        database.use_database(
            "INSERT INTO users (token, username, email, github_url, logo_url, type) VALUES (?, ?, ?, ?, ?, ?)",
            (
                git_token, 
                profile["login"],
                profile["email"],
                profile["html_url"],
                f"https://avatars.githubusercontent.com/u/{git_token}?v=4",
                "GITHUB"
            ),
        )
    
    id = database.use_database(
        "SELECT id FROM users WHERE token = ?",
        (git_token,)
    )[0]

    session["token"] =  git_token
    session["username"] = str(profile["login"])

    session["id"] = id
    session["acct_type"] = "user" #user or business
    
    return redirect("lobby")

import os
import pathlib
from pip._vendor import cachecontrol
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/G_authorize"
)


@authentication.route("/google")
def G_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@authentication.route("/G_authorize")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=G_CLIENT_ID
    )

    print(id_info)



    if not database.user_exists(id_info.get("sub")): 
        database.use_database(
            "INSERT INTO users (token, username, email, logo_url, type) VALUES (?, ?, ?, ?, ?)",
            (
                id_info.get("sub"), 
                id_info.get("name"),
                id_info.get("email"),
                id_info.get("picture"),
                "GOOGLE"
            ),
        )

    session["id"] = database.use_database(
        "SELECT id FROM users WHERE token = ?",
        (id_info.get("sub"),)
    )[0]

    return redirect("/lobby")