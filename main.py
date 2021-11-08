#Documentation - 

from flask import *
import json, time
from flask.scaffold import F
import jsonpickle
import threading
import hashlib
import re
from flask import Flask, abort
import werkzeug
import json as simplejson

app = Flask(__name__)

adminlogin = [{"id":1,"username":"admin","password":"5beeda424743c7f363e567660764a030"}]
group = [{""}]

#Defining the lists.
with open('info.json', 'r') as f:
    group = json.load(f)

#Function to ajust the id value once a user is deleted.
def assignId(lists):        
    for i,q in enumerate(lists):
        idvalue = len(lists)
        return idvalue

#List the users.
@app.route('/listAll/', methods=['GET']) 
def list_page():
    global group
    info = request.get_json() 
    #print("the group value in listall is ",group)       
    json_dump = jsonpickle.encode(group)
    return json_dump

#Add users to the list.
@app.route('/username/', methods=['POST'])
def addOne():
    info = request.get_json()
    username = info["username"] 
    for i in range(len(group)):
        #Check if the username is already being used.
        if group[i]["username"] == username:
            output = {"that username is already taken, please try another"}
            json_dump = jsonpickle.encode(output)
            return json_dump

    #Check for special characters and capital letters.
    if not re.match("^[a-z]*$", info["username"]):
        output = {"your username has to be lower case letters from A-Z and numbers, no special characters"}
        json_dump = jsonpickle.encode(output)
        return json_dump
            
    #Check if the username inputed is more than 15 characters.
    elif len(info["username"]) > 15:
        output = {"your username has too many letters, the limit is 15 characters"}
        json_dump = jsonpickle.encode(output)
        return json_dump

    #If above is clear, hash password and add it to the list.
    else:  
        password = info["password"]
        salt = ("diD_h12$j")
        password += salt
        hashed = hashlib.md5(password.encode())  
        hashed = hashed.hexdigest()
        info["password"] = hashed
        info["id"] = len(group)+1               
        group.append(info)
        output = {"the username and password has been added to the list"}
        json_dump = jsonpickle.encode(output)
        return json_dump

    
            
#Delete all the users data from the list.
@app.route("/deleteAll/", methods=["POST"])
def delete():
    info = request.get_json()

    #Ensure that the admin has to be signed in.
    if info == ("admin"):
        #Deleting everything but the admin.
        with open('info.json', 'w') as f:
            f.seek(0)
            simplejson.dump(adminlogin, f)
        global group
        group = adminlogin  
        output = {"everything but the admin account is deleted"}
        json_dump = jsonpickle.encode(output)
        return json_dump
    
    #Error check if no admin tag.
    else:
        output = {"everything not saved is deleted"}
        json_dump = jsonpickle.encode(output)
        return json_dump

#Sign in section.
@app.route("/SignIn/", methods=["GET"])
def signin():
    info = request.get_json()
    password = info["password"] #Must have "admin" in the tag.
    salt = ("diD_h12$j")
    password += salt
    hashed = hashlib.md5(password.encode()) 
    hashed = hashed.hexdigest()
    info["password"] = hashed
    for i in range(len(group)):   
        #Check if the password and username are correct.
        if group[i]["password"] == info["password"] and group[i]["username"] == info["username"]:
            output = {"successfully signed in"}
            json_dump = jsonpickle.encode(output)
            return json_dump
    else:
        #Error check for incorrect username and password.
        output = {"wrong username or password"}
        json_dump = jsonpickle.encode(output)
        return json_dump
    
#Delete specific user.
@app.route("/DeleteUser/", methods=["DELETE"])
def DeleteSelect():
    info = request.get_json()
    id = info["id"]    
    for i in range(len(group)):
        if id == group[i]["id"]:
            output = {"the user was found and deleted"}
            group.pop(i)
            addition = assignId(group)
            idtest = 1
            #Correct the id tag once user is deleted.
            for y in range(len(group)):
                group[y]["id"] = idtest
                idtest+=1
            json_dump = jsonpickle.encode(output)
            return json_dump

    #Error check if the id is wrong. 
    output = {"the id provided doesnt exist in the list, try requesting the list"}
    json_dump = jsonpickle.encode(output)
    return json_dump

#Saving the information to the file named info.json.
@app.route("/SaveInfo/", methods=["GET"])
def SaveInformation():
    with open('info.json', 'w') as f:
        f.seek(0)        
        f.truncate()    
        simplejson.dump(group, f)
        output = {"The list has been updated"}
        json_dump = jsonpickle.encode(output)
        return json_dump

#Update the login information.
@app.route("/UpdateLogin/", methods=["POST"])
def ChangeInfo():
    info = request.get_json()
    username = info["username"]
    password = info["password"]
    salt = ("diD_h12$j")
    password += salt
    hashed = hashlib.md5(password.encode()) 
    hashed = hashed.hexdigest()
    info["password"] = hashed
    for i in range(len(group)):

        #Updating the information.
        if group[i]["username"] == username and group[i]["password"] == info["password"]:
            if group[i]["username"] == "admin":
                output = {"sorry you are not allowed to change the admin details"}
                json_dump = jsonpickle.encode(output)
                return json_dump 
            newpassword = info["newpassword"]
            salt = ("diD_h12$j")
            newpassword += salt
            hashed = hashlib.md5(newpassword.encode()) 
            hashed = hashed.hexdigest()
            group[i]["password"] = hashed
            output = {"IT WORKED"}
            json_dump = jsonpickle.encode(output)
            return json_dump

    #If the user isnt found.
    else:
        output = {"sorry no username and password was found"}
        json_dump = jsonpickle.encode(output)
        return json_dump


#Check if the error is to do with how the information is implemented.
@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'Please read the documentation something went wrong :/', 400

if __name__ == '__main__':
    app.run(port=5000)