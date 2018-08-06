from flask import Flask
from flask import render_template
from flask import request
import bcrypt
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html', msg="Hello 123!")

@app.route("/user/login", methods=['GET', 'POST'])
def login():
    success = ''
    error = ''

    if (request.method == 'POST'):
        # msg = bcrypt.hashpw(password, bcrypt.gensalt())

        username = request.form['username']
        password = request.form['password']

        if (len(username) == 0):
            error = 'Username is a required field'

        user = findUser(username)
        if (user == None):
            error = 'User ' + username + ' not found'

        if (len(password) == 0):
            error = 'Password is a required field'

        if bcrypt.checkpw(password.encode('utf8'), user['password'].encode('utf8')) == False:
            error = 'Invalid password'
        else:
            success = 'Login successful for user ' + username

    if (len(error) > 0):
        return render_template('login.html', error=error)
    else:
        return render_template('login.html', success=success)

@app.route("/user/register")
def register():
    msg = ''
    
    if (request.method == 'POST'):
        msg = 'submitted'

    return render_template('register.html', msg=msg)

def readJson():
    with open('users.json') as json_file:
        data = json.load(json_file)
        return data

def findUser(username):
    for u in readJson()['users']:
        if (u['username'] == username):
            return u