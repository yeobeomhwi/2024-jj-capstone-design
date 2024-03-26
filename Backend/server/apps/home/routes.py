# -*- encoding: utf-8 -*-
import os
import cv2
from datetime import datetime
from flask import request, jsonify, session, send_file
from werkzeug.utils import secure_filename

''' Import Apps Module '''
from apps.home import blueprint
from apps.home.face_module import predict_face
from apps.home.personal_color_moudle import analysis
from apps.home.user_module import *
from apps.home.admin_module import *


''' Import DB '''
from apps import db
from apps.authentication.models import Users

@blueprint.route('/index')
def index():
    return ""

''' Start User Section '''
@blueprint.route('/register/<path:subpath>', methods = ['GET', 'POST'])
def register(subpath) :
    path_type = subpath.split("/")
    return register_module(path_type)
   
@blueprint.route('/login')
def login() :
    return login_module()

@blueprint.route('/reset_password')
def reset_password() :
    return reset_password_module()

@blueprint.route('/change_password')
def change_password() :
    return change_password_module()

''' End User Section '''
 
''' Start Face Section '''
@blueprint.route('/face', methods = ['GET', 'POST'])
def face() :
    face_image = request.files['face_image']
    upload_dir = "upload/predict/"
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    filename = secure_filename(face_image.filename)
    if len(filename.split(".")) == 1 :
        filename = "noname." + filename.split(".")[-1]
    file_path = os.path.join(upload_dir, filename)
    try:
        face_image.save(file_path)
    except Exception as e:
        return jsonify(result = "fail", type = "save_image", message = str(e))
    
    result = (predict_face(file_path))
    return jsonify(result = "success", type = "face", face = str(result))

@blueprint.route("/distance", methods = ['GET', 'POST'])
def distnace() :
    focal_length = 950
    known_width = 18.0
    face_width_pixels = 200

    def distance_to_camera(known_width, focal_length, face_width):
        return (known_width * focal_length) / face_width
    
    distance_image = request.files['distance_image']
    upload_dir = "upload/distance/"
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    filename = secure_filename(distance_image.filename)

    if len(filename.split(".")) == 1 :
        filename = "noname." + filename.split(".")[-1]

    file_path = os.path.join(upload_dir, filename)

    try:
        distance_image.save(file_path)
    except Exception as e:
        return jsonify(result = "fail", type = "save_image", message = str(e))
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    distance_image = cv2.imread(file_path)
    gray = cv2.cvtColor(distance_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    result_distance = 0
    for (x, y, w, h) in faces:
        result_distance = distance_to_camera(known_width, focal_length, w)

    if result_distance == 0 :
        return jsonify(result = "fail", type = "distance", distance = 0)
    else :
        return jsonify(result = "success", type = "distance", distance = result_distance)

@blueprint.route("/personal_color", methods = ['GET', 'POST'])
def personal_color() :
    face_image = request.files['face_image']
    upload_dir = "upload/personal/"
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    filename = secure_filename(face_image.filename)

    if len(filename.split(".")) == 1 :
        filename = "noname." + filename.split(".")[-1]

    file_path = os.path.join(upload_dir, filename)

    try:
        face_image.save(file_path)
    except Exception as e:
        return jsonify(result = "fail", type = "save_image", message = str(e))
    
    tone = analysis(file_path)
    return jsonify(result = "success", type = "perosnal_color", tone = tone)

''' End Face Section '''

@blueprint.route('/admin/<path:subpath>', methods = ['GET', 'POST'])
def admin(subpath) :
    path_type = subpath.split("/")
    return admin_module(path_type)

@blueprint.route('/widgets')
def widgets():
    widget_names = {}
    widget_list = Widget.query.all()
    for i in widget_list :
        widget_names[i.id] = i.widget_name
    return jsonify(result = "success", type = "widget_list", message = widget_names)

''' For development image upload function with android '''
@blueprint.route('/development_image', methods = ['GET', 'POST'])
def development_image() :
    face_image = request.files['image']
    upload_dir = "upload/development_image/"
    try : 
        username = session['username']
    except :
        return jsonify(result = "fail", type = "development_image", message = "Not Loggined")
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    filename = secure_filename(face_image.filename)
    current_time = (datetime.now().strftime("%Y%m%d%H%M%S"))
    filename = str(username) + "_" + current_time + "." + filename.split(".")[-1]
    
    file_path = os.path.join(upload_dir, filename)
    try:
        face_image.save(file_path)
    except Exception as e:
        return jsonify(result = "fail", type = "development_image", message = str(e))
    return jsonify(result = "success", type = "development_image", message = "")

@blueprint.route('/view_image', methods = ['GET', 'POST'])
def view_image() :
    upload_dir = "upload/development_image/"
    image_lists = os.listdir(upload_dir)
    image_info = []
    for i in image_lists :
        image_info.append([os.path.getsize(upload_dir + i), "https://jj.system32.kr/download_image/" + i])
    image_dict = dict(zip(image_lists, image_info))
    return jsonify(result = "success", type = "view_image", message = image_dict)

@blueprint.route('/download_image/<path:subpath>')
def download_image(subpath) :
    upload_dir = "../upload/development_image/"
    PATH = upload_dir + subpath
    return send_file(PATH, as_attachment=True)

@blueprint.route('/widgets_index')
def widgets_index() :
    return jsonify(result = "success",
                   message = {'weather' : [1, 1],
                              'time' : [1, 2],
                              'login' : [1, 3],
                              'cheerup' : [1, 4]})