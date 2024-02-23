from flask import Flask, jsonify
import time
from time import  strftime
from faker import Faker
import random


nbrUsers = 100
def generateFakeUsers():
    fake = Faker()
    users = []
    for i in range(nbrUsers):
        users.append(fake.name())
    return users

app = Flask(__name__)

userList = generateFakeUsers()

@app.route("/getdata")
def getdata():

    actionList = ["power off", "power on", "low battery"]
    deviceList = ["Footbot Air Quality Monitor", "Amazon Echo", "ecobee4", "Nest T3021US Thermostat", "GreenIQ Controller", "August Doorbell Cam"]

    #mewTime = time.localtime(time.time())
    currentHour = strftime("%I:%M:%S %p", time.localtime(time.time()))
    
    return jsonify({"time":currentHour,"customer": random.choice(userList),"action":random.choice(actionList),"device":random.choice(deviceList)},)




if __name__ == "__main__":
    app.run(debug=True, port=8888)
