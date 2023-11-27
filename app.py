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
    data = data_processing.get_data_trending()
    number_of_videos = len(data[0]["Videos"])
    print(len(data[0]["Videos"]))
    return render_template("trending.html", data=data, number_of_videos=number_of_videos)

@app.route("/performance")
@nocache
def performance():
    last_statistic = data_processing.get_data_performance()[0]
    growth = data_processing.get_data_performance()[2]
    
    listdate = growth['datelist']
    statisticweek = data_processing.statistic_views_perweek(growth['views_perday'])
    
    print(statisticweek)
    listexracted = [] 
    month = data_processing.extract_and_convert_month(listdate[0])

    for i in range(len(listdate)):
        listdate[i] = data_processing.extract_day(listdate[i])
        listexracted.append(str(listdate[i]) + " " + str(month))
    print(listexracted)

    most_viewed = data_processing.get_data_performance()[1][0]["most_views"]
    most_liked = data_processing.get_data_performance()[1][0]["most_likes"]

    #set title just 50 characters
    most_liked["title"] = most_liked["title"][:50] + "..."

    #Format likes and views to be more readable
    most_liked["likeCount"] = data_processing.format_large_number(most_liked["likeCount"])
    most_viewed["viewCount"] = data_processing.format_large_number(most_viewed["viewCount"])

    #dif
    difviewcount = data_processing.get_data_performance()[1][0]["views_growth"]
    difsubscribercount = data_processing.get_data_performance()[1][0]["subs_growth"]


    return render_template("performance.html", most_viewed=most_viewed, most_liked=most_liked, difviewcount=difviewcount, difsubscribercount=difsubscribercount, last_statistic=last_statistic, statisticweek=statisticweek,listexracted=listexracted)

@app.route("/rec-content")
@nocache
def recommendationcontent():
    top10count_key= data_processing.get_top10count_category()[0]
    top10count_value= data_processing.get_top10count_category()[1]
    top10view_key = data_processing.get_top10views_category()[0]
    top10view_value = data_processing.get_top10views_category()[1]
    recomendation = [{"category_id": 10, "category_title": "Music", "predicted_views": 600867622}, {"category_id": 24, "category_title": "Entertainment", "predicted_views": 200969984}, {"category_id": 1, "category_title": "Film & Animation", "predicted_views": 93462335}]
    return render_template("recommendation_content.html", top10count_key=top10count_key, top10count_value=top10count_value, top10view_key=top10view_key, top10view_value=top10view_value, recomendation=recomendation)

@app.route("/rec-channel")
@nocache
def recommendationchannel():
    all_channel_channels = data_processing.get_uniqueChannelsName()
    number_of_channels = len(all_channel_channels)
    data = data_processing.get_data_recommendation_channel()
    rankedbyview = data_processing.sort_by_difviewcount(data)
    rankedbysubscriber = data_processing.sort_by_difsubscount(data)
    rankedbytotalvideo = data_processing.sort_by_diftotalvideo(data)
    return render_template("recommendation_channel.html", all_channel_channels=all_channel_channels, number_of_channels=number_of_channels, rankedbyview=rankedbyview, rankedbysubscriber=rankedbysubscriber, rankedbytotalvideo=rankedbytotalvideo)

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
