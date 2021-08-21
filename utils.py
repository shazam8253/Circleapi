import os
from hashlib import pbkdf2_hmac, sha1
import jwt
from flaskext.mysql import MySQL
from app import db
import boto3, botocore
import os
from werkzeug.utils import secure_filename



access_key = 'AKIAX26ZT7FRENZ3ZO66'
secret_key = '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'
aws_bucket_name = "circlestorage"


s3 = boto3.client(
    "s3",
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key
)


JWT_SECRET_KEY = '$B6cC]UVD@~TMh7P,sb^6w{"t96l,?:aLWXtz(GrQOt7,odlV@3!T\m{Cg$wU4{'

def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False

def generate_salt():
    salt = os.urandom(16)
    return salt.hex()

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()

def db_write(query, params):
    conn = db.connect()
    cursor =conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        return True

    except:
        cursor.close()
        return False

def db_read(query, params=None):
    conn = db.connect()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    entries = cursor.fetchall()
    cursor.close()
    content = []
    for entry in entries:
        content.append(entry)
    return content

def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    print(encoded_content)
    return encoded_content

def validate_user(email, password):
    current_user = db_read("""SELECT * FROM circle.Users WHERE email = %s""", (email))

    if len(current_user) == 1:
        saved_password_hash = current_user[0]["password_hash"]
        saved_password_salt = current_user[0]["password_salt"]
        password_hash = generate_hash(password, saved_password_salt)
        print("Passwords compared")
        print(saved_password_hash)
        print(password_hash)
        if password_hash == saved_password_hash:
            user_id = current_user[0]["idUsers"]
            jwt_token = generate_jwt_token({"id": user_id})
            return jwt_token
        else:
            return False

    else:
        return False

def profpic(jwttoken, file):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    s3 = session.resource('s3')
    userID = jwt.decode(jwttoken, JWT_SECRET_KEY, algorithms=['HS256'])['id']
    print(userID)
    endpoint = '{userid}/profpic/{filename}'.format(userid = userID, filename = str(secure_filename(file.filename)))
    print(endpoint)
    # file_type = file.filename.split('.')[1].lower()
    s3.Bucket(aws_bucket_name).put_object(Body = file, Key = endpoint)


