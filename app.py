import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile
import random
import data_processing
from pymongo import MongoClient

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("index.html", file_path="img/image_here.jpg")

@app.route("/performance")
@nocache
def performance():
    return render_template("performance.html")

@app.route("/rec-content")
@nocache
def recommendationcontent():
    return render_template("recommendation_category.html")

@app.route("/rec-channel")
@nocache
def recommendationchannel():
    return render_template("recommendation_channel.html")

@app.route("/trending")
@nocache
def trending():
    data = data_processing.get_data_trending()
    number_of_videos = len(data[0]["Videos"])
    print(len(data[0]["Videos"]))
    return render_template("trending.html", data=data, number_of_videos=number_of_videos)

@app.route("/trendingfs")
@nocache
def trendingfs():
    data = data_processing.get_data_trending()
    number_of_videos = len(data[0]["Videos"])
    print(len(data[0]["Videos"]))
    return render_template("trending2.html", data=data, number_of_videos=number_of_videos)
    
# #route quiz upload
# @app.route("/quiz_upload", methods=["POST"])
# @nocache
# def quiz_upload():
#     image_path = "static/img/img_now_quiz.jpg"  # Path to your imageresul
#     image_size = image_processing.get_image_size(image_path)
#     rgb_values = image_processing.get_all_rgb(image_path)
#     total_index_rgb = len(rgb_values)
#     target = os.path.join(APP_ROOT, "static/img")
#     if not os.path.isdir(target):
#         if os.name == 'nt':
#             os.makedirs(target)
#         else:
#             os.mkdir(target)
#     for file in request.files.getlist("file"):
#         file.save("static/img/img_now_quiz.jpg")
#     copyfile("static/img/img_now_quiz.jpg", "static/img/img_normal_quiz.jpg")
#     return render_template("quiz_uploaded.html", file_path="img/img_now_quiz.jpg",image_size=image_size,rgb=rgb_values, total_index_rgb=total_index_rgb)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
