from flask import Flask, jsonify, request, render_template
import json
import jwt
import datetime
import random
from functools import wraps
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from datauser import *

# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testst'
mysql = MySQL(app)
table = 'linkedin'

app.config.from_pyfile('config.cfg')
mail = Mail(app)

app.config['SECRET_KEY'] ='dvp'
tmp = []

userData = {
    "email" : '',
    "otp": ''
}

# Token Required
def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if len(tmp) == 0:
            return jsonify({'message':'Token is missing'}),403
        try:
            data = jwt.decode(tmp[0],app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message':'Token is invalid or expired'}),403
        return f(*args,**kwargs)
    return decorated

# Create OTP
def createOTP():
    finalOTP= ''
    for i in range (4):
        finalOTP = finalOTP + str(random.randint(0,9))
    return finalOTP

# Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        if validateUser(username,password):
            token = jwt.encode({'user':username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10)},app.config['SECRET_KEY'])
            tmp.append(token)
            return render_template('login.html',token=token)
        else:
            return('Password atau username salah')
    return render_template('login.html')

# Define what the app does
@app.route("/",methods=['GET','POST'])
@check_token
def index():
    cur = mysql.connection.cursor()
    # query = f'select * from {table} limit 3'
    #profile_picture = 'Dummy1'
    query = f'select * from {table} limit 3'
    cur.execute(query)
    data = cur.fetchall()
    return jsonify(data)

@app.route("/create",methods=['GET','POST'])
def create():
    cur = mysql.connection.cursor()
    query = f'insert into {table} values (2022,"CS","in.linkedin","Dummy","Dummy","Dummy","Dummy","Dummy","Dummy","Dummy","Dummy")'
    cur.execute(query)
    mysql.connection.commit()
    return 'data created'
@app.route('/update',methods=['GET','POST','PUT'])
def update():
    cur = mysql.connection.cursor()
    category = 'CS'
    linkedin = 'in.linkedin'
    profile_picture = 'Dummy1'
    query = f'update {table} set profile_picture = "{profile_picture}" where linkedin ="{linkedin}"'
    cur.execute(query)
    mysql.connection.commit()
    return 'data updated'
@app.route('/delete',methods=['GET','POST','DELETE'])
def delete():
    cur = mysql.connection.cursor()
    profile_picture = 'Dummy1'
    query = f'delete from {table} where profile_picture = "{profile_picture}"'
    cur.execute(query)
    mysql.connection.commit()
    return 'data deleted'

# Send to Email
# https://stackoverflow.com/questions/72547853/unable-to-send-email-in-c-sharp-less-secure-app-access-not-longer-available/72553362#72553362

@app.route('/email',methods=['GET'])
def sendEmail():
    return render_template('email.html')

@app.route('/verify',methods=['GET','POST'])
def verify():
    email = request.form['email']
    userData['email'] = email
    msg = Message('DO NOT SHARE THIS EMAIL!',sender='tes@tes.com',recipients=[email])
    otp = createOTP()
    userData['otp'] = otp
    msg.body = f'Shh, your OTP code is: {otp}'
    print(email)    # untuk tampilan di terminal
    print(otp)      # untuk tampilan di terminal
    mail.send(msg)
    return render_template('otp.html')

@app.route('/validate',methods=['POST'])
def validate():
    userOTP = request.form['otp']
    if userData['otp'] == userOTP:
        token = jwt.encode({'user':userData['email'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10)},app.config['SECRET_KEY'])
        tmp.append(token)
        return 'OTP valid'
    else:
        return 'OTP invalid'