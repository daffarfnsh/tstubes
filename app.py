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

# Define what the app does
@app.get("/")
def index():
    cur = mysql.connection.cursor()
    table = 'linkedin'
    cur.execute(f'''select * from {table} limit 1''')
    data = cur.fetchall()
    return jsonify(data)