"""
Written by Aiden Yoshioka-Miller

This is the main program to run the website and control everything.
I'm not too experienced with MVC with Flask, but this is the structure I saw in the tutorials and guided that I followed. 
Some of the methods are not super efficient, and I have some issues that are mostly on the part of flask that I have no idea on how to solve (SOmetimes the page doesn't reload after a scan).add()
For the most part, this is where all the controller logic and routing is done. The DAL is partially in this, but that's because everything is handled through SQLAlchemy rather than my own methods. 

This code is done by a novice, and will be cleaned up as I get better after I complete my senior year.
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import sqlalchemy
import os, pickle, sys, time

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir + '/tools')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
db = SQLAlchemy(app)
tool_dir = '../tools/'
deauth_process = ""
pid = 0

class device(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    scan_group = db.Column(db.Integer, nullable=False, default=0)
    device_name = db.Column(db.String(50), nullable=False)
    mac_address = db.Column(db.String(17), nullable=False, default='00:00:00:00:00:00') 
    archived = db.Column(db.Boolean, nullable=False , default=False)
    channel = db.Column(db.Integer, nullable=False, default=1)
    date_scanned = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Device ID: ' + str(self.device_id)+ ' Device Name: ' + self.device_name +' Mac Address: ' + self.mac_address + ' Archived: ' + str(self.archived) + ' Channel: ' + str(self.channel) + ' Date: ' + str(self.date_scanned) + ' Scan Group: ' + str(self.scan_group)

#auxilary methods-----------------------------------------------------------------------------------------------------------------------
def monitor_mode(num: int):
    os.system('ifconfig wlan'+num+' down')
    os.system('iwconfig wlan'+num+' mode monitor')
    #os.system('airmon-ng start wlan0 &&')
    time.sleep(2)
    os.system('ifconfig wlan'+num+' up ')

def managed_mode(num: int):
    os.system('ifconfig wlan'+num+' down')
    os.system('iwconfig wlan'+num+' mode managed')
    #os.system('airmon-ng stop wlan0mon &&')
    time.sleep(2)
    os.system('ifconfig wlan'+num+' up ')

#The following two PID methods are for retrieving and setting the global PID because I was having some problems accessing it later on in this file because it wasn't registering it as a global
def set_deauth_pid(num: int):
    print("setting pid to: " + num)
    pid = num
    print("pid: " + get_deauth_pid())
def get_deauth_pid():
    with open('../.files/pid.txt', 'r') as file:
        pid = int(file.read())
    return pid

#This works to find the 
def get_latest_scan_group():
    #getting the latest scan group
    latest_device = device.query.order_by(desc(device.scan_group)).with_entities(device.scan_group).first()
    if(latest_device != None):
        return latest_device.scan_group
    else:
        return 0

#retrives all scans with the highest current scan group. the scan group is incremented whenever a new entry is submitted
def get_latest_scans():
    latest_group = get_latest_scan_group()
    devices = device.query.filter_by(scan_group=latest_group).all()
    return devices

#this retrieves all scans and is only used by the history tab 
def get_all_scans():
    #getting the scans
    return device.query.all()

#This just gets all scans that have been archived
def get_archived_scans():
    #getting the archived scans
    return device.query.filter_by(archived=True).all()

#routes----------------------------------------------------------------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template('index.html')

#Routes to the scan page
@app.route("/scan", methods=['GET', 'POST'])
def display_scan_page():
    if request.method == 'POST':

        #running the scan script 
        monitor_mode(1)
        os.system('python3 ' +tool_dir+ 'scanner.py -i wlan1')
        managed_mode(1)

        #parsing the results
        os.system('python3 ' + tool_dir + 'result_parser.py')

        #reading the results from the .pkl file
        devices = []
        with open('results.pkl', 'rb') as fp:
            devices = pickle.load(fp)

        #getting the latest scan group to set the next scan group
        latest_group_number = get_latest_scan_group() + 1

        #adds all the devices to the database then returns the scan page with a table of results (sometimes this breaks for no reason and doesn't reload the page. However, all results are still submitted)
        for line in devices:
            db.session.add(device(scan_group=latest_group_number, device_name=line["name"], mac_address=line["mac"], channel=line["channel"]))
        try:
            db.session.commit()
            db.session.remove()
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            print(str(e))
            db.session.rollback()

        return render_template('scan.html', scan_results=devices)
        
    else:
        return render_template('scan.html')

#Navigates to the deauth page and displays a table of all the latest scanned devices 
@app.route("/deauth" , methods=['GET', 'POST']) 
def display_deauth_page():
    p = ""
    latest_scans = get_latest_scans()
    if request.method == 'POST':
        #starting the subprocess
        try:
            #opening a subprocess that runs my script that runs the deauth script with minimal input
            deauth_process = subprocess.Popen([sys.executable, '../tools/deauther_short.py' , "-t " + request.form['selected'] + " "], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)   
            
            #writing the process's pid to a file because python refuses to change the global PID value outside this method
            with open('../.files/pid.txt', 'w') as file:
                file.write(str(deauth_process.pid))
            print("Deauth pid: " + str(get_deauth_pid()))
        except:
            print("Failed to start deauth")
        return render_template('deauth.html', devices=latest_scans, deauthing=request.form['selected'])
    else:
        #if the page is loaded, it tries to 
        try:
            if (get_deauth_pid() != os.getpid() and get_deauth_pid() != 0):
                print("killing: " + str(get_deauth_pid()))
                os.system("kill -9 " + str(get_deauth_pid()))
 
        except:
            #print(str(deauth_process.pid))
            print("Deauth failed pid: " + str(get_deauth_pid()))
            print("failed to kill process")
        return render_template('deauth.html', devices=latest_scans)

#History page is here just to show all previous scans
@app.route("/history" ,methods=["GET", "POST"])
def display_history_page():
    if request.method == 'POST':
        if("archive" in request.form):
            #getting device ID from form
            device_to_archive_id = request.form['device_id']
            #updating the device's archive value
            device_to_archive = device.query.filter_by(device_id=device_to_archive_id).first()
            device_to_archive.archived=True
        elif("clear" in request.form):
            device.query.filter_by(archived=False).delete()
        else:
            print("removing")
            #getting device ID from form
            device_to_archive_id = request.form['device_id']
            #getting device ID from form
            device_to_unarchive_id=request.form['device_id']
            device_to_unarchive = device.query.filter_by(device_id=device_to_unarchive_id).first()
            device_to_unarchive.archived=False
        
        try:
            db.session.commit()
            #db.session.remove()
        except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as e:
            print(str(e))
            db.session.rollback()
        return render_template('history.html',archived=get_archived_scans(), scans=get_all_scans())
    else:
        return render_template('history.html',archived=get_archived_scans(), scans=get_all_scans())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=80)