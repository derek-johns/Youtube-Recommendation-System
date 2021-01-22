import csv
import glob
import re
import pandas as pd
import time
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
import requests, sys, time, os, argparse
from datetime import datetime, timedelta
from airflow.hooks.mysql_hook import MySqlHook


temp_youtube_trending_vids = '/temp/temp_youtube_trending_vids.csv'
temp_youtube_trending_key = 'youtube-trending/{{ ds }}_US_videos.csv'
BUCKET_NAME = 'youtube-trending'
API_KEY = 'AIzaSyBSW9yzjTd5yHWdYXU-teE7MKDKVdAW9KQ'
OUTPUT_FILE = ''
country_codes = ['US']


def local_to_mysql():

    connection = MySqlHook(mysql_conn_id='youtube_db')
    query = '''
        CREATE TABLE IF NOT EXISTS `group3`.`youtube7` (
          `video_id` VARCHAR(100) NOT NULL,
          `title` VARCHAR(100) NULL,
          `publishedAt` VARCHAR(45) NULL,
          `channelId` VARCHAR(45) NULL,
          `channelTitle` VARCHAR(60) NULL,
          `categoryId` INT NULL,
          `trending_date` DATETIME NULL,
          `tags` LONGTEXT NULL,
          `view_count` INT NULL,
          `likes` INT NULL,
          `dislikes` INT NULL,
          `comment_count` INT NULL,
          `thumbnail_link` VARCHAR(100) NULL,
          `comments_disabled` TINYINT NULL,
          `ratings_disabled` TINYINT NULL,
          `description` LONGTEXT NULL,
           PRIMARY KEY (`video_id`));
    '''
    connection.run(query, autocommit=True)
    # df = pd.read_csv(temp_youtube_trending_vids)
    df = pd.concat([pd.read_csv(f, sep=',') for f in glob.glob('/temp' + "/*.csv")],
                   ignore_index=True)
    df = df.where((pd.notnull(df)), None)
    for i, row in df.iterrows():
        query = '''
            INSERT IGNORE INTO group3.youtube7 (video_id, title, publishedAt, channelId, channelTitle, categoryId,
            trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled,
            description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        try:
            connection.run(query, autocommit=True, parameters=tuple(row))
        except:
            pass


def remove_local_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        logging.info(f'File {filename} not found')


snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle",
                    "categoryId"]

unsafe_characters = ['\n', '"']
# Used to identify columns, currently hardcoded order
header = ["video_id"] + snippet_features + ["trending_date", "tags", "view_count", "likes", "dislikes",
                                            "comment_count", "thumbnail_link", "comments_disabled",
                                            "ratings_disabled", "description"]


def prepare_feature(feature):
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(page_token, country_code):
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={API_KEY}"
    request = requests.get(request_url)
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    return request.json()


def get_tags(tags_list):
    return prepare_feature("|".join(tags_list))


def get_videos(items):
    lines = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False
        if "statistics" not in video:
            continue
        video_id = prepare_feature(video['id'])
        snippet = video['snippet']
        statistics = video['statistics']
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        trending_date = time.strftime("%y-%m-%d")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = statistics.get("viewCount", 0)
        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0
        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
        else:
            comments_disabled = True
            comment_count = 0
        line = [video_id] + features + [prepare_feature(x) for x in [trending_date, tags, view_count, likes, dislikes,
                                                                       comment_count, thumbnail_link, comments_disabled,
                                                                       ratings_disabled, description]]
        lines.append(",".join(line))
    return lines


def get_pages(country_code, next_page_token="&"):
    country_data = []
    while next_page_token is not None:
        video_data_page = api_request(next_page_token, country_code)
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token
        items = video_data_page.get('items', [])
        country_data += get_videos(items)
    return country_data


def write_to_file(country_code, country_data):
    print(f"Writing {country_code} data to file...")
    with open(f"/temp/temp_youtube_trending_vids.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")


def get_data():
    print('GET DATA')
    for country_code in country_codes:
        country_data = [",".join(header)] + get_pages(country_code)
        write_to_file(country_code, country_data)


hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

country_code = 'US'
api_name = 'search'

related_snippet_features = ["title",
                    "channelId",
                    "channelTitle",
                    ]
related_unsafe_characters = ['\n', '"']
related_header = ["video_id"] + related_snippet_features + ["categoryId", "duration", "thumbnail_link", "tags", "description",
                                            "channel_desc", "channel_keywords", "related_vid_id"]


def related_api_request(page_token, vid_id):
    request_url = f"https://www.googleapis.com/youtube/v3/{api_name}?part=snippet{page_token}relatedToVideoId={vid_id}&type=video&regionCode=US&maxResults=50&key={API_KEY}"
    request = requests.get(request_url)
    print('RELATED API REQUEST')

    return request.json()

# '/temp/temp_youtube_trending_vids.csv'
# trending_file = open(f'/temp/temp_youtube_trending_vids.csv', mode = 'r', encoding = 'utf8')


def related_prepare_feature(feature):
    for ch in related_unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def related_get_tags(tags_list):
    return prepare_feature("|".join(tags_list))


def create_vid_id_list(trend_file):
    ret_list = list()
    print(trend_file)
    for index, row in trend_file.iterrows():
        ret_list.append(row['video_id'])
    return ret_list


def related_get_pages(vid_id, next_page_token="&"):
    country_data = []

    while next_page_token is not None:
        video_data_page = related_api_request(next_page_token, vid_id)
        # if video_data_page == -1:
        #     print('BLOCKED')
        #     break
        next_page_token = video_data_page.get("nextPageToken", None)
        next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token
        items = video_data_page.get('items', [])
        country_data += related_get_videos(vid_id, items)
        # time.sleep(2)
    country_data = [",".join(related_header)] + country_data
    related_write_to_file(country_code, country_data, vid_id)


def related_write_to_file(c_code, country_data, vid_id):
    with open(f"/temp/temp_youtube_related_vids_{vid_id}.csv", "w+", encoding='utf-8') as file:
        for row in country_data:
            file.write(f"{row}\n")


def related_get_videos(orig_vid_id, items):
    lines = []
    for video in items:
        if 'snippet' not in video:
            continue
        video_id = video['id']['videoId']
        snippet = video['snippet']
        description = snippet.get("description", "")
        channel_id = snippet.get('channelId')
        features = [prepare_feature(snippet.get(feature, "")) for feature in related_snippet_features]
        duration, category_id, tags = get_youtube_video_duration(video_id)
        channel_desc, channel_keywords = get_channel_info(channel_id)

        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")

        line = [video_id] + features + [related_prepare_feature(x) for x in
                                        [category_id, duration, thumbnail_link, tags, description, channel_desc,
                                         channel_keywords, orig_vid_id]]
        lines.append(",".join(line))

    return lines


def get_youtube_video_duration(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id={video_id}&key={API_KEY}"
    # tags = ["none"]
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
        tags = related_get_tags(snippet.get("tags", ["[none]"]))
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
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=brandingSettings&id={channel_id}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    channel_settings = data['items'][0]['brandingSettings']['channel']
    description = channel_settings.get('description', "")
    keywords = channel_settings.get('keywords', "")
    description = related_prepare_feature(description)
    ret_keys = related_prepare_feature(keywords)
    return description, ret_keys


def create_files():
    print('CREATE FILES')
    # trend_dict = csv.DictReader(temp_youtube_trending_vids)
    trend_dict = pd.read_csv(temp_youtube_trending_vids)
    vid_ids = create_vid_id_list(trend_dict)
    for i in vid_ids:
        related_get_pages(i)


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id='youtube-trending',
    default_args=default_args,
    schedule_interval='50 11 * * *',
    max_active_runs=1
)

start_of_pipeline = DummyOperator(task_id='start_of_pipeline', dag=dag)

fetch_video_data_from_api= PythonOperator(
    task_id='fetch_video_data_from_api',
    python_callable=get_data,
    dag=dag
)

upload_to_rds = PythonOperator(
    task_id='upload_to_rds',
    python_callable=local_to_mysql,
    dag=dag
)

remove_local_csv = PythonOperator(
    dag=dag,
    task_id='remove_local_csv',
    python_callable=remove_local_file,
    op_kwargs={
        'filename': temp_youtube_trending_vids
    }
)

load_related_videos = PythonOperator(
    dag=dag,
    task_id='load_related_videos',
    python_callable=create_files
)

end_of_pipeline = DummyOperator(task_id='end_of_pipeline', dag=dag)

start_of_pipeline >> fetch_video_data_from_api >> load_related_videos >> upload_to_rds >> remove_local_csv >> end_of_pipeline


