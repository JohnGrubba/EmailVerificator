from flask import Flask, redirect
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask("app")
CORS(app)

# Configure Swagger UI
SWAGGER_URL = "/docs"
API_URL = "/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Email Verificator"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

hds = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}


@app.route("/")
def home():
    return redirect("/docs")


@app.route("/swagger.json")
def swaager():
    return open("swagger.json", "r").read()


@app.route("/api/new")
def new_email():
    r = requests.get("http://ese.kr/?pb=6549")
    soup = BeautifulSoup(r.text, "html.parser")
    element = soup.find("input", {"type": "search", "name": "mailbox"})
    return {"email": element["value"]}


@app.route("/api/mailbox/<string:email>")
def insta_verif(email):
    data = "mail_id=&mail_mode=&lang=en&mailbox=" + email
    r = requests.post("http://ese.kr/", data=data, headers=hds).text
    soup = BeautifulSoup(r, "html.parser")
    emails = []
    for element in soup.findChildren("tr")[1:]:
        children = element.findChildren(string=True)
        if len(children) >= 3:
            emails.append(
                {
                    "sender": children[0],
                    "subject": children[1],
                    "timestamp": children[2],
                }
            )
    return emails


app.run(host="0.0.0.0", port=8080)
