from flask import Flask
from flask import render_template
from flask import request
import bcrypt
import json
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user/login", methods=['GET', 'POST'])
def login():
    success = ''
    error = ''
    code = ''

    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        if (len(username) == 0):
            error = 'Username is a required field'

        user = findUser(username)
        if (user == None):
            error = 'User ' + username + ' not found'

        if bcrypt.checkpw(password.encode('utf8'), user['password'].encode('utf8')) == True:
            code = random.randint(1000,9999)

            # Update the user record with the code
            updateUser(username, None, code)

            success = ('Login successful for user ' + username 
                + '. To complete the login, use the code "%s" on the following page.') % code
        else:
            error = 'Invalid password'

    if (len(error) > 0):
        return render_template('login.html', error=error)
    else:
        return render_template('login.html', success=success)

@app.route("/user/register", methods=['GET', 'POST'])
def register():
    error = ''
    success = ''
    
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']

        if (len(username) == 0):
            error = 'Username is a required field'

        if (len(password) == 0):
            error = 'Password is a required field'

        if (addUser(username, password) == True):
            success = 'User registered successfully!'
        else:
            error = 'Error registering user!'

    if (len(error) > 0):
        return render_template('register.html', error=error)
    else:
        return render_template('register.html', success=success)

@app.route('/user/code', methods=['GET', 'POST'])
def code():
    error = ''
    success = ''

    if (request.method == 'POST'):
        username = request.form['username']
        code = request.form['code']
        user = findUser(username)

        if not code:
            code = None

        if (secureCompare(code, user['code']) == True):
            success = "Success! You're now logged in as " + username
        else:
            error = 'Error with the code provided'

    if (len(error) > 0):
        return render_template('code.html', error=error)
    else:
        return render_template('code.html', success=success)

def readJson():
    with open('users.json') as json_file:
        data = json.load(json_file)
        return data

def writeJson(data):
    with open('users.json', 'w') as f:
        json.dump(data, f)

    return True

def addUser(username, password):
    data = readJson()
    newUser = {
        'username': username,
        'password': bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
        'code': 'None'
    }
    data['users'].append(newUser)
    return writeJson(data)

def updateUser(username, password=None, code=None):
    data = readJson()
    for u in data['users']:
        if u['username'] == username:
            if (password != None):
                u['password'] = password

            if (code != None):
                u['code'] = code
    
    writeJson(data)
    return True

def findUser(username):
    for u in readJson()['users']:
        if (u['username'] == username):
            return u

def secureCompare(input1, input2):
    bytes1 = bytearray(str(input1))
    bytes2 = bytearray(str(input2))

    return len(bytes1) == len(bytes2)