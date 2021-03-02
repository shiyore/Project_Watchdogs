from flask import Flask
app = Flask(__name__)

def factors(num):
    return [x for x in range (1, num+1) if num%x==0]

@app.route("/")
def home():
    return ("<a href='/factors/100'>CLick here for an example</a>")

@app.route("/factors/<int:n>")
def factors_display(n):
    list_factor = factors(int(n))

    html = "<h1> Factors of " + str(n) + " are</h1>\n<ul>"

    for f in list_factor :
        html += "<li>" + str(f) + "</li>\n"
    html += "</ul>"
    return html

if __name__ == '__main__' :
    app.run(host='0.0.0.0')
