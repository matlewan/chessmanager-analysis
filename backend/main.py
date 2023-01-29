from flask import Flask, redirect
from update import update
from process import process
from os import environ

app = Flask(__name__)
inp = 'data.json'
out = environ.get("OUTPUT_FILE")

@app.route("/update")
def hello_world():
    return '<form action="/api/make_update" method="POST"><input type="submit" value="Update" /></form>'

@app.route("/make_update", methods=["GET", "POST"])
def update_data():
    update(inp)
    process(inp, out)
    return redirect("https://pomysl.mateuszdev.com")
