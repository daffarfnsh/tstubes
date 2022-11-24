from flask import Flask, jsonify, request
import json
from flask_mysqldb import MySQL
# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testtst'
mysql = MySQL(app)


# print(data)


# Define what the app does
@app.get("/")
def index():
    cur = mysql.connection.cursor()
    table = 'estimated_crimes_1979_2019'
    cur.execute(f'''select * from {table} limit 5''')
    data = cur.fetchall()
    return jsonify(data)