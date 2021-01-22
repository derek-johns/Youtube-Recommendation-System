from shutil import copy2
import mysql.connector
import pandas as pd
import glob
import os


def dataframe():
    path = '/Users/sheng/Youtube-Recommendation-System/related'
    dest = '/Users/sheng/Youtube-Recommendation-System/related_backup'
    df = pd.concat([pd.read_csv(f, sep=',') for f in glob.glob(path + "/*.csv")],
                   ignore_index=True)
    df = df.where((pd.notnull(df)), None)

    if not os.path.exists('related_backup'):
        os.makedirs('related_backup')

    for f in glob.glob(path + "/*.csv"):
        copy2(f, dest)
        os.remove(f)
    return df


def export():
    db = mysql.connector.connect(user='group3',
                                 password='ZCW+G3+data1-2',
                                 host='ls-981afae8457656b0e311a4599e509521975ea3c7.c13c4sg7cvg0.us-east-2.rds.amazonaws.com',
                                 database='group3')
    cursor = db.cursor()
    create_youtube_table_query = """
        CREATE TABLE IF NOT EXISTS `group3`.`related_videos` (
          `video_id` VARCHAR(100) NOT NULL,
          `title` VARCHAR(100) NULL,
          `channelId` VARCHAR(45) NULL,
          `channelTitle` VARCHAR(60) NULL,
          `categoryId` INT NULL,
          `duration` INT NULL,
          `thumbnail_link` VARCHAR(100) NULL,
          `tags` LONGTEXT NULL,
          `description` LONGTEXT NULL,
          `channel_desc` LONGTEXT NULL,
          `channel_keywords` LONGTEXT NULL,
          `related_vid_id` VARCHAR(100) NOT NULL,
          PRIMARY KEY (`video_id`, `related_vid_id`));
        """
    cursor.execute(create_youtube_table_query)
    db.commit()

    df = dataframe()

    for i, row in df.iterrows():
        sql = """INSERT IGNORE INTO group3.related_videos (video_id, title, channelId, channelTitle, categoryId,
         duration, thumbnail_link, tags, description, channel_desc, channel_keywords, related_vid_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, tuple(row))
        db.commit()
    db.close()


if __name__ == "__main__":
    export()
