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

# Count views,subcription, videoCount for Recommendation channel
def get_views_channels():
    # Assuming you have a MongoDB connection
    client = MongoClient('localhost', 27017)
    db = client['A2']
    collection = db['StatisticChannels']

    # Find all documents with ChannelsTitle equal to "Pricebook"
    first_document = collection.find({"ChannelsTitle": "Pricebook"}).limit(1)
    first_document = list(first_document)

    last_document = collection.find({"ChannelsTitle": "Pricebook"}).sort([('_id', -1)]).limit(1)
    last_document = list(last_document)

    first_document2 = list(collection.find({"ChannelsTitle": "Channels1"}).limit(1))
    last_document2 = list(collection.find({"ChannelsTitle": "Channels1"}).sort([('_id', -1)]).limit(1))

    first_document += first_document2
    last_document += last_document2

    view_count_first_document = int(first_document[1]["ChannelStatistics"]["viewCount"])
    view_count_last_document = int(last_document[1]["ChannelStatistics"]["viewCount"])

    views = view_count_last_document - view_count_first_document
    print(views)
    # print(view_count_first_document)
    # print(view_count_last_document)
    
    return last_document

# def get_subscriber_channels():
# def get_videoCount_channels(): 