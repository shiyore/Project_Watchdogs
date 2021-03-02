# hello world with flask
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return ('Hello')

@app.route("/test")
def test():
    return("This is a test")

@app.route("/Welcome/<name>")
def welcome_name(name):
    return("<h1 Style='colour:#00ffaa;'> Welcome, " + name + "!</h1>")

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
