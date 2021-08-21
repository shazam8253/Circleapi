import profile
from flask import Blueprint, request, Response, jsonify
from werkzeug.utils import secure_filename
from utils import db_write, profpic


profile = Blueprint("profile", __name__)
@profile.route("/profilepic", methods=["POST"])
def uploadprofpic():
    if 'image' not in request.files:
        print('No file part')
        return Response(status=250)
    profilepic = request.files['image']
    if profilepic:
        print("image sent")
        profpic( request.headers.get('Authorization'), profilepic)
        # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTJ9.V0KLsRHxxfFpDZwnwrCwrgYWJjLNTWJeX865Z8Ns6wE"
        return Response(status=200)
    else:
        return Response(status=250)


