import profile
from flask import Blueprint, request, Response, jsonify
from werkzeug.utils import secure_filename
from utils import db_write, getallzeposts, postuno, profpic


profile = Blueprint("profile", __name__)
@profile.route("/profilepic", methods=["POST"])
def uploadprofpic():
    if 'image' not in request.files:
        print('No file part')
        return Response(status=250)
    profilepic = request.files['image']
    if profilepic:
        print("image sent")
        try: 
            profpic( request.headers.get('Authorization'), profilepic)
            return Response(status = 200)
        except:
            return Response(status = 250)
        # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTJ9.V0KLsRHxxfFpDZwnwrCwrgYWJjLNTWJeX865Z8Ns6wE"
    else:
        return Response(status=250)

@profile.route("/post", methods=["POST"])
def post():
    if 'image' not in request.files:
        print('No file part')
        return Response(status=250)
    post = request.files['image']
    if post:
        print("image sent")
        try: 
            postuno(request.headers.get('Authorization'), post)
            return Response(status = 200)
        except:
            return Response(status = 250)
        # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTJ9.V0KLsRHxxfFpDZwnwrCwrgYWJjLNTWJeX865Z8Ns6wE"
    else:
        return Response(status=250)

@profile.route("/getallposts", methods=['GET'])
def getallposts():
    try:
        end = jsonify({'posts': getallzeposts(request.headers.get('Authorization'))})
        print(end)
        return end
    except:
        return Response(status = 250)



