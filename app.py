from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_cors import CORS, cross_origin
# from flask_s3 import FlaskS3





app = Flask(__name__)
CORS(app)
db = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Circle123'
app.config['MYSQL_DATABASE_HOST'] = 'circle.cqilqaim3php.us-east-1.rds.amazonaws.com'
# app.config['FLASKS3_BUCKET_NAME'] = 'mybucketname'

db.init_app(app)

from blueprint_auth import authentication
from profile import profile
app.register_blueprint(authentication, url_prefix="/api/auth")
app.register_blueprint(profile, url_prefix="/api/profile")


# # cursor.execute("SELECT * FROM circle.Users")
# # data = cursor.fetchone()
# # print(data)

# @app.route('/users/account', methods=['POST', 'DELETE', 'PATCH', 'GET'])
# def account():
#     if request.method == 'POST':
#         conn = db.connect()
#         cursor =conn.cursor()
#         content = request.json
#         insert_user_cmd = """INSERT INTO circle.Users (username, password, email, firstname, lastname) VALUES (%s, %s, %s, %s, %s)"""
#         cursor.execute(insert_user_cmd, (content["username"], content['password'], content['email'], content['firstname'], content['lastname']))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify("Success")

#     if request.method == 'DELETE':
#         conn = mysql.connect()
#         cursor =conn.cursor()
#         content = request.json
#         insert_user_cmd = """DELETE FROM circle.Users WHERE (idUsers = %s);"""
#         cursor.execute(insert_user_cmd, (content["id"]))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return jsonify("Success")

#     if request.method == 'GET':
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         content = request.json
#         insert_user_cmd = """SELECT * FROM circle.Users WHERE (idUsers = %s);"""
#         cursor.execute(insert_user_cmd, (content["id"]))
#         rows = cursor.fetchall()
#         cursor.close()
#         conn.close()
#         return jsonify(rows)

#     # if request.method == 'PATCH':
#     #     conn = mysql.connect()
#     #     cursor =conn.cursor()
#     #     content = request.json
#     #     insert_user_cmd = """DELETE FROM circle.Users WHERE (idUsers = %s);"""
#     #     cursor.execute(insert_user_cmd, (content["id"]))
#     #     conn.commit()
#     #     cursor.close()
#     #     conn.close()
#     #     return jsonify("Success")



# @app.route('/users/account', methods=['POST', 'DELETE', 'PATCH', 'GET'])


if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
