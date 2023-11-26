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

def get_data_performance():
    client = MongoClient('localhost', 27017)
    db = client['A2']
    collection = db['StatisticChannels']

    query = {
    "ChannelsTitle": "CSSGOSS",
    }
    
    performancedata = []
    allstatistic = collection.find(query).sort([('_id', -1)]).limit(7)
    allstatistic = list(allstatistic)
    allstatistic = sorted(allstatistic, key=lambda x: x['_id'], reverse=False)

    firstdocumentstatistic = allstatistic[0]["ChannelStatistics"]
    print(firstdocumentstatistic)

    # get all views Count per day
    views_perday = []  
    datelist = []

    #append all viewCount per day
    for i in range(len(allstatistic)):
        views_perday.append(allstatistic[i]["ChannelStatistics"]["viewCount"])
        datelist.append(allstatistic[i]["Date"])

    #Structur
    structurperweek = ({
        "views_perday": views_perday,
        "datelist": datelist
    })
    # get all video data
    allvideostatistic = []

    for i in range(len(allstatistic)-1):
        allvideostatistic.append(allstatistic[i]["Videos"])

    # Flatten the list of video data
    flat_video_data = [video for videos_list in allvideostatistic for video in videos_list]

    # # Find the video with the most viewCount
    video_with_most_views = get_most_viewed_video(flat_video_data)
    video_with_most_likes = get_most_liked_video(flat_video_data)
    
    # Sort the results by "Date" in descending order and limit to one document
    lastdocumentstatistic = collection.find(query).sort([('_id', -1)]).limit(1)
    lastdocumentstatistic = list(lastdocumentstatistic)
    lastdocumentstatistic = lastdocumentstatistic[0]["ChannelStatistics"]
        
    client.close()

    # Calculate the difference between the last and first document
    lastdocumentstatistic["viewCount"] = int(lastdocumentstatistic["viewCount"])
    lastdocumentstatistic["subscriberCount"] = int(lastdocumentstatistic["subscriberCount"])
    firstdocumentstatistic["viewCount"] = int(firstdocumentstatistic["viewCount"])
    firstdocumentstatistic["subscriberCount"] = int(firstdocumentstatistic["subscriberCount"])

    difviewcount = lastdocumentstatistic["viewCount"] - firstdocumentstatistic["viewCount"]
    difsubscribercount = lastdocumentstatistic["subscriberCount"] - firstdocumentstatistic["subscriberCount"]

    performancedata.append({
        "most_views": video_with_most_views,
        "most_likes": video_with_most_likes,
        "views_growth": difviewcount,
        "subs_growth": difsubscribercount
    })

    return lastdocumentstatistic,performancedata,structurperweek


def format_large_number(number):
    suffixes = ["", " Ribu", " Juta", " Milyar", " Triliun"]  # Add more suffixes as needed

    if number < 1000:
        return str(int(number))

    exp = int((len(str(int(number))) - 1) / 3)
    rounded_number = round(number / (1000.0 ** exp), 1)

    formatted_number = f"{int(rounded_number) if rounded_number.is_integer() else rounded_number}{suffixes[exp]}"
    return formatted_number

def get_uniqueChannelsName():
    client = MongoClient('localhost', 27017)
    db = client['A2']
    collection = db['StatisticChannels']

    #find unique channel name
    uniqueChannelsName = collection.distinct("ChannelsTitle")
    client.close()

    return uniqueChannelsName

def get_most_viewed_video(listdata):
    return max(listdata, key=lambda x: x['viewCount'])

def get_most_liked_video(listdata):
    return max(listdata, key=lambda x: x['likeCount'])

def statistic_views_perweek(data):
    daily_differences = []
    daily_differences.append(data[0])
    for i in range(1, len(data)):
        value_today = int(data[i])
        value_yesterday = int(data[i - 1])
        difference = value_today - value_yesterday
        daily_differences.append(difference)
    return daily_differences

def get_data_recommendation_channel():
    client = MongoClient('localhost', 27017)
    db = client['A2']
    collection = db['StatisticChannels']

    query = {
    "ChannelsTitle": "CSSGOSS",
    }

    allstatchannel = []
    allfirststatchannel = []
    alllaststatchannel = []
    difsubscribercount = []
    difviewcount = []
    diftotalvideo = []
    allchannel = ['CSSGOSS','GadgetIn']
    
    for i in range(len(allchannel)):
        query = {
        "ChannelsTitle": allchannel[i],
        }
        allstatistic = collection.find(query).sort([('_id', -1)]).limit(7)
        allstatistic = list(allstatistic)
        allstatistic = sorted(allstatistic, key=lambda x: x['_id'], reverse=False)
        allfirststatchannel.append(allstatistic[0]["ChannelStatistics"])
        if len(allstatistic) == 7:
            alllaststatchannel.append(allstatistic[6]["ChannelStatistics"])
        else:
            alllaststatchannel.append("no data")
        
    for i in range(len(allchannel)):
        if alllaststatchannel[i] != "no data":
            alllaststatchannel[i]["viewCount"] = int(alllaststatchannel[i]["viewCount"])
            alllaststatchannel[i]["subscriberCount"] = int(alllaststatchannel[i]["subscriberCount"])
            alllaststatchannel[i]["videoCount"] = int(alllaststatchannel[i]["videoCount"])

            allfirststatchannel[i]["viewCount"] = int(allfirststatchannel[i]["viewCount"])
            allfirststatchannel[i]["subscriberCount"] = int(allfirststatchannel[i]["subscriberCount"])
            allfirststatchannel[i]["videoCount"] = int(allfirststatchannel[i]["videoCount"])

            difviewcount.append(alllaststatchannel[i]["viewCount"] - allfirststatchannel[i]["viewCount"])
            difsubscribercount.append(alllaststatchannel[i]["subscriberCount"] - allfirststatchannel[i]["subscriberCount"])
            diftotalvideo.append(alllaststatchannel[i]["videoCount"] - allfirststatchannel[i]["videoCount"])
        else:
            difviewcount.append("no data")
            difsubscribercount.append("no data")
            diftotalvideo.append("no data")

    structurdif = ({
        "channel": allchannel,
        "difviewcount": difviewcount,
        "difsubscribercount": difsubscribercount,
        "diftotalvideo": diftotalvideo
    })

    return structurdif

def sort_by_difviewcount(data):
    # Zip the lists into a list of tuples
    zipped_data = zip(data['channel'], data['difviewcount'], data['difsubscribercount'], data['diftotalvideo'])

    # Sort the list of tuples based on the difviewcount (index 1)
    sorted_data = sorted(zipped_data, key=lambda x: x[1] if isinstance(x[1], (int, float)) else float('-inf'), reverse=True)

    # Unzip the sorted data
    sorted_channel, sorted_difviewcount, sorted_difsubscribercount, sorted_diftotalvideo = zip(*sorted_data)

    # Create a new dictionary with the sorted data
    sorted_dict = {
        'channel': list(sorted_channel),
        'difviewcount': list(sorted_difviewcount),
        'difsubscribercount': list(sorted_difsubscribercount),
        'diftotalvideo': list(sorted_diftotalvideo),
    }

    return sorted_dict

def sort_by_difsubscount(data):
    # Zip the lists into a list of tuples
    zipped_data = zip(data['channel'], data['difviewcount'], data['difsubscribercount'], data['diftotalvideo'])

    # Sort the list of tuples based on the difviewcount (index 1)
    sorted_data = sorted(zipped_data, key=lambda x: x[2] if isinstance(x[2], (int, float)) else float('-inf'), reverse=True)

    # Unzip the sorted data
    sorted_channel, sorted_difviewcount, sorted_difsubscribercount, sorted_diftotalvideo = zip(*sorted_data)

    # Create a new dictionary with the sorted data
    sorted_dict = {
        'channel': list(sorted_channel),
        'difviewcount': list(sorted_difviewcount),
        'difsubscribercount': list(sorted_difsubscribercount),
        'diftotalvideo': list(sorted_diftotalvideo),
    }

    return sorted_dict

def sort_by_diftotalvideo(data):
    # Zip the lists into a list of tuples
    zipped_data = zip(data['channel'], data['difviewcount'], data['difsubscribercount'], data['diftotalvideo'])

    # Sort the list of tuples based on the difviewcount (index 1)
    sorted_data = sorted(zipped_data, key=lambda x: x[3] if isinstance(x[3], (int, float)) else float('-inf'), reverse=True)

    # Unzip the sorted data
    sorted_channel, sorted_difviewcount, sorted_difsubscribercount, sorted_diftotalvideo = zip(*sorted_data)

    # Create a new dictionary with the sorted data
    sorted_dict = {
        'channel': list(sorted_channel),
        'difviewcount': list(sorted_difviewcount),
        'difsubscribercount': list(sorted_difsubscribercount),
        'diftotalvideo': list(sorted_diftotalvideo),
    }

    return sorted_dict