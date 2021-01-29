import csv
import os
import requests
import time
import json
import re
from datetime import timedelta

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

country_code='US'
api_key=''
api_name='search'

snippet_features = ["title",
                    "channelId",
                    "channelTitle",
                    ]
unsafe_characters = ['\n', '"']
header = ["video_id"] + snippet_features + ["categoryId", "duration", "thumbnail_link", "tags", "description", "channel_desc", "channel_keywords", "related_vid_id"]

def api_request(page_token, vid_id):
    request_url = f"https://www.googleapis.com/youtube/v3/{api_name}?part=snippet{page_token}relatedToVideoId={vid_id}&type=video&regionCode=US&maxResults=50&key={api_key}"
    request = requests.get(request_url)
    return request.json()
    
trending_file = open(r'C:\Python\Youtube proj\Youtube-Recommendation-System\21.13.01_US_videos2.csv', mode='r', encoding='utf8')

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
        country_data += get_videos(vid_id, items)
    country_data = [",".join(header)] + country_data
    write_to_file(country_code, country_data, vid_id)

def write_to_file(country_code, country_data,vid_id):
    with open(f"{time.strftime('%y.%d.%m')}_{country_code}_related_to_{vid_id}.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")

def get_videos(orig_vid_id, items):
    lines = []
    for video in items:
        if 'snippet' not in video:
            continue
        video_id = video['id']['videoId']
        snippet = video['snippet']
        description = snippet.get("description", "")
        channel_id = snippet.get('channelId')
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]
        duration, category_id, tags = get_youtube_video_duration(video_id)
        channel_desc, channel_keywords = get_channel_info(channel_id)

        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        

        line = [video_id] + features + [prepare_feature(x) for x in [category_id, duration, thumbnail_link, tags, description, channel_desc, channel_keywords, orig_vid_id]]
        lines.append(",".join(line))
    return lines

def get_youtube_video_duration(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id={video_id}&key={api_key}"
    tags = ["none"]
    response = requests.get(url) 
    data = response.json() 
    items = data.get('items', [])
    video_seconds = 0
    category = 0
    tags = []
    if len(items) != 0:
        snippet = data['items'][0]['snippet']
        duration = data['items'][0]['contentDetails']['duration']
        category = data['items'][0]['snippet']['categoryId']
        tags = get_tags(snippet.get("tags", ["[none]"]))
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        video_seconds = str(timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds())
        return video_seconds, category, tags
    
    return video_seconds, category, tags

def get_channel_info(channel_id):
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=brandingSettings&id={channel_id}&key={api_key}"
    response = requests.get(url) 
    data = response.json()
    items = data.get('items', [])
    description = ""
    ret_keys = []
    if len(items) != 0:
        branding = items[0]['brandingSettings']
        channel_settings = branding.get('channel',[])
        description=channel_settings.get('description',"")
        keywords = channel_settings.get('keywords',"")
        description = prepare_feature(description)
        ret_keys = prepare_feature(keywords)
        return description, ret_keys
    return description, ret_keys

trend_dict = csv.DictReader(trending_file)
vid_ids = create_vid_id_list(trend_dict)
def create_files():
    trend_dict = csv.DictReader(trending_file)
    vid_ids = create_vid_id_list(trend_dict)
    for id in vid_ids:
        get_pages(id)

get_pages(vid_ids[0])