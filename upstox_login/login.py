from flask import Flask, request
import os
import requests
import webbrowser
import json
import config

app = Flask(__name__)

TOKEN_FILE = r"D:\UPSTOX_MCX\token.json"
print("Saving token to:", os.path.abspath(TOKEN_FILE))

@app.route("/callback")
def callback():

    code = request.args.get("code")

    token_url = "https://api.upstox.com/v2/login/authorization/token"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "code": code,
        "client_id": config.API_KEY,
        "client_secret": config.API_SECRET,
        "redirect_uri": config.REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(
        token_url,
        headers=headers,
        data=data
    )

    token_data = response.json()

    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=4)

    return """
    <h2>Login Successful</h2>
    <h3>token.json saved.</h3>
    You can close this browser window.
    """

def open_login():

    auth_url = (
        "https://api.upstox.com/v2/login/authorization/dialog"
        f"?response_type=code"
        f"&client_id={config.API_KEY}"
        f"&redirect_uri={config.REDIRECT_URI}"
    )

    webbrowser.open(auth_url)

if __name__ == "__main__":

    print("Opening Upstox Login...")

    open_login()

    app.run(
        host="127.0.0.1",
        port=8080,
        debug=False
    )