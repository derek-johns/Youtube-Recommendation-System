import csv
import os
import requests
import time
import json
import re

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

country_code='US'
api_key=os.environ.get('ytkey')
api_name='search'
i=0
snippet_features = ["title",
                    "channelId",
                    "channelTitle",
                    ]
unsafe_characters = ['\n', '"']
header = ["video_id"] + snippet_features + ["categoryId", "duration", "thumbnail_link", "tags"]

def api_request(page_token, vid_id):
    request_url = f"https://www.googleapis.com/youtube/v3/{api_name}?part=snippet{page_token}relatedToVideoId={vid_id}&type=video&regionCode=US&maxResults=50&key={api_key}"
    request = requests.get(request_url)
    return request.json()
    
trending_file = open(r'C:\Python\Youtube proj\Youtube-Recommendation-System\output\trending_vids.csv', mode='r', encoding='utf8')

def prepare_feature(feature):
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'

def get_tags(tags_list):
    return prepare_feature("|".join(tags_list))

def create_vid_id_list(trend_file):
    ret_list = list()
    for row in trend_file:
        ret_list.append(row['video_id'])
    return ret_list

def get_pages(vid_id, next_page_token="&"):
    country_data = []

    while next_page_token is not None:
        video_data_page = api_request(next_page_token, vid_id)
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token
        items = video_data_page.get('items', [])
        country_data += get_videos(items)
    country_data = [",".join(header)] + country_data
    write_to_file(country_code, country_data, vid_id)

def write_to_file(country_code, country_data,vid_id):
    with open(f"{time.strftime('%y.%d.%m')}_{country_code}_related_to_{vid_id}.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")

def get_videos(items):
    lines = []
    for video in items:
        if 'snippet' not in video:
            continue
        video_id = video['id']['videoId']
        snippet = video['snippet']
        features = [snippet.get(feature, "") for feature in snippet_features]
        duration, category_id = get_youtube_video_duration(video_id)
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        tags = get_tags(snippet.get("tags", ["[none]"]))

        line = [video_id] + features + [category_id, duration, thumbnail_link, tags]
        lines.append(",".join(line))
    return lines

def get_youtube_video_duration(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id={video_id}&key={api_key}"

    response = requests.get(url) 
    data = response.json() 

    duration = data['items'][0]['contentDetails']['duration']
    category = data['items'][0]['snippet']['categoryId']
    hours = hours_pattern.search(duration)
    minutes = minutes_pattern.search(duration)
    seconds = seconds_pattern.search(duration)
    hours = int(hours.group(1)) if hours else 0
    minutes = int(minutes.group(1)) if minutes else 0
    seconds = int(seconds.group(1)) if seconds else 0
    time=(f'{hours}:{minutes}:{seconds}')
    return time, category 

trend_dict = csv.DictReader(trending_file)
vid_ids = create_vid_id_list(trend_dict)
get_pages(vid_ids[0])
# for id in vid_ids:
#     get_pages(id)