from flask import Flask, jsonify, request, render_template
import json
import jwt # Perlu install pip3 install PyJWT diawal
import datetime
from functools import wraps
from flask_mysqldb import MySQL
from datauser import *

# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testst'
mysql = MySQL(app)
table = 'linkedin'

app.config['SECRET_KEY'] ='dvp'
storage = []
# Token Required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if len(storage) == 0:
            return jsonify({'message':'Tokekn is missing'}),403
        try:
            data = jwt.decode(storage[0],app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message':'Token is invalid'}),403
        return f(*args,**kwargs)
    return decorated
    
#Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        if checkValidation(username,password):
            token = jwt.encode({'user':username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=10)},app.config['SECRET_KEY'])
            storage.append(token)
            return render_template('login.html',token=token)
        else:
            return('Password atau username salah')
    return render_template('login.html')

# Define what the app does
@app.route("/",methods=['GET','POST'])
@token_required
def index():
    cur = mysql.connection.cursor()
    # query = f'select * from {table} limit 3'
    profile_picture = 'Dummy1'
    query = f'select * from {table} limit 1'
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