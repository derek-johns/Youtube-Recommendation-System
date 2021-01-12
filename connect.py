from shutil import copy2
import mysql.connector
import pandas as pd
import glob
import os


def dataframe():
    path = '/Users/sheng/Youtube-Recommendation-System/output'
    dest = '/Users/sheng/Youtube-Recommendation-System/backup'
    df = pd.concat([pd.read_csv(f, sep=',') for f in glob.glob(path + "/*.csv")],
                   ignore_index=True)
    df = df.where((pd.notnull(df)), None)

    if not os.path.exists('backup'):
        os.makedirs('backup')

    for f in glob.glob(path + "/*.csv"):
        copy2(f, dest)
        os.remove(f)
    return df


def export():
    db = mysql.connector.connect(user='group3',
                                 password='',
                                 host='',
                                 database='group3')
    cursor = db.cursor()
    create_youtube_table_query = """
        CREATE TABLE IF NOT EXISTS `group3`.`youtube3` (
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
        """
    cursor.execute(create_youtube_table_query)
    db.commit()

    df = dataframe()

    for i, row in df.iterrows():
        # sql = """INSERT INTO group3.youtube2 (video_id, title, publishedAt, channelId, channelTitle, categoryId,
        #  trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled,
        #   description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE VALUES
        #   (video_id=%s, title=%s, publishedAt=%s, channelId=%s, channelTitle=%s, categoryId=%s, trending_date=%s, tags=%s,
        #    view_count=%s, likes=%s, dislikes=%s, comment_count=%s, thumbnail_link=%s, comments_disabled=%s, ratings_disabled=%s,
        #    description=%s)"""
        # sql = """
        # INSERT INTO group3.youtube3 (video_id, title, publishedAt, channelId, channelTitle, categoryId,
        # trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled,
        # ratings_disabled, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        # ON DUPLICATE KEY UPDATE VALUES (video_id=VALUES(video_id), title=VALUES(title), publishedAt=VALUES(publishedAt),
        # channelId=VALUES(channel_id), channelTitle=VALUES(channelTitle), categoryId=VALUES(categoryId),
        # trending_date=VALUES(trending_date), tags=VALUES(tags), view_count=VALUES(view_count), likes=VALUES(likes),
        # dislikes=VALUES(dislikes), comment_count=VALUES(comment_count), thumbnail_link=VALUES(thumbnail_link),
        # comments_disabled=VALUES(comments_disabled), ratings_disabled=VALUES(ratings_disabled),
        # description=VALUES(description))
        # """
        sql = """INSERT IGNORE INTO group3.youtube3 (video_id, title, publishedAt, channelId, channelTitle, categoryId,
         trending_date, tags, view_count, likes, dislikes, comment_count, thumbnail_link, comments_disabled, ratings_disabled,
          description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, tuple(row))
        db.commit()
    db.close()


if __name__ == "__main__":
    export()
