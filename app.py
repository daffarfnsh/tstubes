from flask import Flask, jsonify, request, render_template
import json
from flask_mysqldb import MySQL
# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testtst'
mysql = MySQL(app)
table = 'estimated_crimes_1979_2019'
# print(data)


# Define what the app does
@app.route("/",methods=['GET','POST'])
def index():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        form = request.form
        year = form['year']
        if not year:
            cur.execute(f'''select * from {table} limit 10''')
            data = cur.fetchall()
            return render_template('index.html',data = data)
        cur.execute(f'select * from {table} where year = {year} limit 10')
        data = cur.fetchall()
        return render_template('index.html',data = data)
    cur.execute(f'''select * from {table} limit 10''')
    data = cur.fetchall()
    return render_template('index.html',data = data)

@app.route("/create",methods=['GET','POST'])
def create():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        form = request.form
        year = form['year']
        stateAbbr = form['state_abbr']
        stateName = form['state_name']
        query = f'insert into {table} (year,state_abbr,state_name) values ({year},"{stateAbbr}","{stateName}")'
        cur.execute(query)
        print(query)
        mysql.connection.commit()
        return 'success'

    return render_template('create.html')
@app.route('/update',methods=['GET','POST'])
def update():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        form = request.form
        year = form['year']
        stateAbbr = form['state_abbr']
        stateName = form['state_name']
        query = f'update {table} set state_name = "{stateName}" where year = {year} and state_abbr ="{stateAbbr}"'
        cur.execute(query)
        print(query)
        mysql.connection.commit()
    return render_template('update.html')
@app.route('/delete',methods=['GET','POST'])
def delete():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        form = request.form
        year = form['year']
        query = f'delete from {table} where year = {year}'
        cur.execute(query)
        print(query)
        mysql.connection.commit()
    return render_template('delete.html')