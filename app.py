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
    linkedin = 'www.linkedin.com'
    query = f'select * from {table} limit 1'
    # query = f'select * from {table} where linkedin = "{linkedin}"'
    cur.execute(query)
    data = cur.fetchall()
    return jsonify(data)

@app.route("/create",methods=['GET','POST'])
def create():
    cur = mysql.connection.cursor()
    index = 2022
    category = 'CS'
    linkedin = 'www.linkedin.com'
    query = f'insert into {table} values ({index},"{category}","{linkedin}","a","b","c","d","e","f","g","h")'
    cur.execute(query)
    mysql.connection.commit()
    return 'data created'
@app.route('/update',methods=['GET','POST','PUT'])
def update():
    cur = mysql.connection.cursor()
    index = 2022
    category = 'CS'
    linkedin = 'www.linkedin.com/'
    query = f'update {table} set linkedin = "{linkedin}" where index = {index} and category ="{category}"'
    cur.execute(query)
    mysql.connection.commit()
    return 'data updated'
@app.route('/delete',methods=['GET','POST','DELETE'])
def delete():
    cur = mysql.connection.cursor()
    linkedin = 'www.linkedin.com'
    query = f'delete from {table} where linkedin = "{linkedin}"'
    cur.execute(query)
    mysql.connection.commit()
    return 'data deleted'