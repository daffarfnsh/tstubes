
text/x-generic app.py ( Python script, ASCII text executable )
from appflask import app
from config import mysql
# from datauser import *

from flask import Flask, jsonify, request, render_template, make_response
from functools import wraps
from urllib.request import urlopen
from flaskext.mysql import MySQL
import requests
import json
import jwt
import datetime
import random
import pymysql

@app.route('/')
def index():
    data = {'message':"Selamat datang di layanan Pengelolaan Data LinkedIn"}
    return jsonify(data)

app.config['SECRET_KEY'] ='dvp'
# tmp = []

# Token Required
def check_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is Missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

        except:
            return jsonify({'message': 'Token is Invalid'}), 403

        return f(*args, **kwargs)
    return decorated
    
# Login Account
@app.route('/login',methods=['GET','POST'])
def login():
    auth = request.authorization
    if auth and validate(auth.username, auth.password) == True:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])

        return jsonify({'Token': token})

    return make_response('Failed to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
def validate(username, password):
    valid = False
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM user_data_dr where username = '{username}' and password = '{password}'")
    if cursor.rowcount > 0:
        valid = True
    cursor.close()
    conn.close()
    return valid

def partner_login():
    url = 'http://rakha:password@wipeeeb.my.id/manage-job-applicants/login'
    response = requests.get(url)
    response = (response.json())    
    token = response['Token']
    return token
    
def me_login():
    url = 'http://rakha:password@wipeeeb.my.id/test/login'
    response = requests.get(url)
    response = (response.json())    
    token = response['Token']
    return token

# Define the app
@app.route("/read",methods=['GET','POST'])
@check_token
def read():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select id, Name, category, clean_skills from linkedin_dafeb limit 5")
    data = cursor.fetchall()
    return jsonify(data)

# Penyedia(s)
@app.route('/jobseekers/<locationpick>/<fcategory>/<lcategory>')
@check_token
def getJobseekers(locationpick, fcategory, lcategory):
    arrParameter = []
    arrPositionParameter = []
    if str(locationpick) != 'f':
        arrParameter += [str(locationpick)]
        arrPositionParameter += [1]
    if str(fcategory) != 'f':
        if str(lcategory) != 'f':
            arrParameter += [str(str(fcategory)+" "+str(lcategory))]
            arrPositionParameter += [3]
        else:
            arrParameter += [str(fcategory)]
            arrPositionParameter += [2]
    if str(lcategory) != 'f':
        if str(fcategory) != 'f':
            arrParameter += [str(str(fcategory)+" "+str(lcategory))]
            arrPositionParameter += [3]
        else:
            arrParameter += [str(lcategory)]
            arrPositionParameter += [3]

        
    queryselect = "SELECT Name, description, category, location, clean_skills FROM linkedin_dafeb WHERE"

    querycondition = ""
    for i in range(len(arrParameter)):
        if arrPositionParameter[i] == 1:
            if i != 0:
                querycondition = querycondition + " AND "
            querycondition = querycondition + " location LIKE '% " + arrParameter[i] + "' "
        if arrPositionParameter[i] == 2:
            if i != 0:
                querycondition = querycondition + " AND "
            querycondition = querycondition + "  category LIKE '" + arrParameter[i] + "%' "
        if arrPositionParameter[i] == 3:
            if i != 0:
                querycondition = querycondition + " AND "
            querycondition = querycondition + " category LIKE '%" + arrParameter[i] + "' "

    queryfinal = queryselect + querycondition
    # return jsonify(queryfinal)  
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(queryfinal)
        read_row = cursor.fetchall()
        response = jsonify(read_row)
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify(e)
    finally:
        cursor.close()
        conn.close()

# @app.route('/jobseekers-by-category/<categorypick>')
# @check_token
# def getJobseekerByCategory(categorypick):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Name, description, location, clean_skills FROM linkedin_dafeb WHERE category = '{categorypick}'")
#         data = cursor.fetchall()
#         return jsonify(data)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()
        
# @app.route('/jobseekers-by-location/<locationpick>')
# @check_token
# def getJobseekerByLocation(locationpick):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Name, description, category, clean_skills FROM linkedin_dafeb WHERE location LIKE '% {locationpick}'")
#         data = cursor.fetchall()
#         return jsonify(data)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()
        
# @app.route('/jobseekers-by-category/<categorypick>/<locationpick>')
# @check_token
# def getJobseekerByCategoryLocation(categorypick, locationpick):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Name, description, clean_skills FROM linkedin_dafeb WHERE category = '{categorypick}' AND location LIKE '% {locationpick}'")
#         data = cursor.fetchall()
#         return jsonify(data)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()
        
# @app.route('/jobseekers-by-location/<locationpick>/<categorypick>')
# @check_token
# def getJobseekerByLocationCategory(locationpick, categorypick):
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute(f"SELECT Name, description, clean_skills FROM linkedin_dafeb WHERE location LIKE '% {locationpick}' AND category = '{categorypick}'")
#         data = cursor.fetchall()
#         return jsonify(data)
    
#     except Exception as e:
#         print(e)
#         return jsonify({"msg" : "Data tidak ditemukan"})
    
#     finally:
#         cursor.close()
#         conn.close()

# Partner Connect
@app.route('/job_lists_view')
def jobListView():
    token = partner_login()
    url = "http://wipeeeb.my.id/manage-job-applicants/read?token=" + str(token)
    dataresponse = urlopen(url)
    dataresponse = json.loads(dataresponse.read())
    return jsonify(dataresponse)

@app.route('/job_lists/<locationpick>/<fcategory>/<lcategory>')
def jobList(locationpick,fcategory,lcategory):
    token = partner_login()
    url = "http://wipeeeb.my.id/manage-job-applicants/getJob/" + locationpick + "/" + fcategory + "/" + lcategory + "?token=" + str(token)
    dataresponse = urlopen(url)
    dataresponse = json.loads(dataresponse.read())
    return jsonify(dataresponse)

@app.route('/job_lists/<locationpick>/<fcategory>/<lcategory>/estimate')
def estimate(locationpick, fcategory, lcategory):
    arrTitle = []
    dctEstimate = []
    token = partner_login()
    url = "http://wipeeeb.my.id/manage-job-applicants/getJob/" + locationpick + "/" + fcategory + "/" + lcategory + "?token=" + str(token)
    dataresponse = urlopen(url)
    dataresponse = json.loads(dataresponse.read())
    n = len(dataresponse)
    for data in dataresponse:
        x = data['Title']
        arrTitle.append(x)
    
    for i in range(n):
        dctEstimate[i] = str(random.randint(20,60))

    return jsonify({"Title":arrTitle, "Estimate":dctEstimate})
    # my_token = me_login()
    # my_url = "http://wipeeeb.my.id/test/jobseekers/" + locationpick + "/" + fcategory + "/" + lcategory + "?token=" + str(my_token)
    # my_data = urlopen(my_url)
    # my_data = json.loads(my_data.read())
    # n = len(my_data)
    # for data in my_data:
    #     x = data['Name']
    #     arrName.append(data)
    # return jsonify({"Title":arrTitle, "Name":arrName, "Estimate"=dctEstimate})
    
# @app.route('/job_rec_category/<categorypick>')
# def jobRecCategory(categorypick):
#     token = partner_login()
#     url = "http://wipeeeb.my.id/manage-job-applicants/get-jobs-by-category/" + categorypick + "?token=" + str(token)
#     dataresponse = urlopen(url)
#     dataresponse = json.loads(dataresponse.read())
#     return jsonify(dataresponse)

# @app.route('/job_rec_location/<locationpick>')
# def jobRecLocation(locationpick):
#     token = partner_login()
#     url = "http://wipeeeb.my.id/manage-job-applicants/get-jobs-by-category/" + locationpick + "?token=" + str(token)
#     dataresponse = urlopen(url)
#     dataresponse = json.loads(dataresponse.read())
#     return jsonify(dataresponse)


if __name__ == "__main__":
    app.run()