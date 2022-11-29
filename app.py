from flask import Flask, jsonify, request
import json
from flask_mysqldb import MySQL
# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testst'
mysql = MySQL(app)
table = 'linkedin'


# Define what the app does
@app.route("/",methods=['GET','POST'])
def index():
    cur = mysql.connection.cursor()
    # query = f'select * from {table} limit 3'
    profile_picture = 'Dummy1'
    query = f'select * from {table} where profile_picture = "{profile_picture}"'
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