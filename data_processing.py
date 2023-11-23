import numpy as np
from pymongo import MongoClient
from datetime import datetime


def get_data_trending():
    client = MongoClient('localhost', 27017)
    db = client['A2']
    collection = db['Trending']

    last_document = collection.find().sort([('_id', -1)]).limit(1)
    last_document = list(last_document)
    
    client.close()
    print(last_document[0]["Videos"][0])
    # print(last_document[0])
    # add month to each video
    for video in last_document[0]["Videos"]:
        video["Month"] = extract_and_convert_month(video["PublishedDate"])
        video["Day"] = extract_day(video["PublishedDate"])

    return last_document

def get_publish_date_day(video):
    published_at_str = video.get('Published At')
    if published_at_str:
        published_at = datetime.strptime(published_at_str, '%Y-%m-%dT%H:%M:%SZ')
        return published_at.day

def extract_and_convert_month(date_string):
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_string, '%Y-%m-%d')

    # Get the month as an integer (e.g., 10 for October)
    month_number = date_object.month

    # Define a mapping of month numbers to their abbreviated names
    month_mapping = {
        1: 'Jan', 2: 'Feb', 3: 'Mar',
        4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep',
        10: 'Okt', 11: 'Nov', 12: 'Dec'
    }

    # Convert the month number to its abbreviated name
    month_name = month_mapping.get(month_number, str(month_number))

    # Return the formatted month string
    return month_name

def extract_day(date_string):
    # Convert the date string to a datetime object
    date_object = datetime.strptime(date_string, '%Y-%m-%d')

    # Get the month as an integer (e.g., 10 for October)
    day_number = date_object.day

    # Return the formatted month string
    return day_number


def get_data_performance():
    client = MongoClient('localhost', 27017)
    db = client['A2']
    collection = db['StatisticChannels']

    query = {
    "ChannelsTitle": "CSSGOSS",
    }
    
    allstatistic = collection.find(query)
    allstatistic = list(allstatistic)

    allvideostatistic = []

    for i in range(len(allstatistic)):
        allvideostatistic.append(allstatistic[i]["Videos"])

    # Flatten the list of video data
    flat_video_data = [video for videos_list in allvideostatistic for video in videos_list]

    # Find the video with the most viewCount
    video_with_most_views = max(flat_video_data, key=lambda x: x['viewCount'])
    video_with_most_likes = max(flat_video_data, key=lambda x: x['likeCount'])

    # Sort the results by "Date" in descending order and limit to one document
    sort_order = [("Date", -1)]  # -1 for descending order
    lastdocumentstatistic = collection.find(query).sort(sort_order).limit(1)
    lastdocumentstatistic = list(lastdocumentstatistic)
    lastdocumentstatistic = lastdocumentstatistic[0]["ChannelStatistics"]

    #first document
    firstdocumentstatistic = collection.find(query).limit(1)
    firstdocumentstatistic = list(firstdocumentstatistic)
    firstdocumentstatistic = firstdocumentstatistic[0]["ChannelStatistics"]
    
    client.close()

    # Calculate the difference between the last and first document
    lastdocumentstatistic["viewCount"] = int(lastdocumentstatistic["viewCount"])
    lastdocumentstatistic["subscriberCount"] = int(lastdocumentstatistic["subscriberCount"])
    firstdocumentstatistic["viewCount"] = int(firstdocumentstatistic["viewCount"])
    firstdocumentstatistic["subscriberCount"] = int(firstdocumentstatistic["subscriberCount"])

    difviewcount = lastdocumentstatistic["viewCount"] - firstdocumentstatistic["viewCount"]
    difsubscribercount = lastdocumentstatistic["subscriberCount"] - firstdocumentstatistic["subscriberCount"]

    return lastdocumentstatistic, video_with_most_views, video_with_most_likes, difviewcount, difsubscribercount


def format_large_number(number):
    suffixes = ["", " Ribu", " Juta", " Milyar", " Triliun"]  # Add more suffixes as needed

    if number < 1000:
        return str(int(number))

    exp = int((len(str(int(number))) - 1) / 3)
    rounded_number = round(number / (1000.0 ** exp), 1)

    formatted_number = f"{int(rounded_number) if rounded_number.is_integer() else rounded_number}{suffixes[exp]}"
    return formatted_number
