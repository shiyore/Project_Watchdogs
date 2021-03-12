"""
Written by Aiden Yoshioka-Miller

This is the main program to run the website and control everything
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import os, pickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
db = SQLAlchemy(app)
tool_dir = '../../.tools/'

class device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False, default='00:00:00:00:00:00') 
    ip_address = db.Column(db.String(15), nullable=True, default='1.1.1.1')
    device_type = db.Column(db.Integer, nullable=False, default=0)
    archived = db.Column(db.Boolean, nullable=False , default=False)
    channel = db.Column(db.Integer, nullable=False, default=1)
    date_scanned = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Device Name: ' + self.device_name +' Mac Address: ' + self.mac_address + ' IP Address: ' + self.ip_address 

def monitor_mode():
    os.system('ifconfig wlan0 down')
    os.system('iwconfig wlan0 mode monitor')
    os.system('ifconfig wlan0 up ')

def managed_mode():
    os.system('ifconfig wlan0 down')
    os.system('iwconfig wlan0 mode managed')
    os.system('ifconfig wlan0 up ')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/scan", methods=['GET', 'POST'])
def display_scan_page():
    if request.method == 'POST':

        #running the scan script 
        monitor_mode()
        os.system('python3 ' +tool_dir+ 'scanner.py -i wlan0')
        managed_mode()

        #parsing the results
        os.system('python3 ' + tool_dir + 'result_parser.py')

        devices = []
        with open('results.pkl', 'rb') as fp:
            devices = pickle.load(fp)

        for line in devices:
            db.session.add(device(device_name=line["name"], mac_address=line["mac"], channel=line["channel"]))
        try:
            db.session.commit()
            db.session.remove()
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            print(str(e))
            db.session.rollback()
        return render_template('scan.html', scan_results=devices)
        
    else:
        return render_template('scan.html')

@app.route("/deauth" , methods=['GET', 'POST']) 
def display_deauth_page():
    if request.method == 'POST':
        return render_template('deauth.html', deauthing=request.form['exampleRadios1'])
    else:
        return render_template('deauth.html')

@app.route("/")

@app.route("/history" ,methods=["GET", "POST"])
def display_history_page():
    if request.method == 'POST':
        #later this will add a post to the database
        return render_template('history.html')
    else:
        #later, this will pass database data to the view
        return render_template('history.html')


if __name__ == "__main__":
    app.run(debug=True)