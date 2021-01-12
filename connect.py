import mysql.connector
import pandas as pd
import glob
import os


db = mysql.connector.connect(user='group3',
                            password='',
                            host='',
                            database='group3')
cursor = db.cursor()
create_youtube_table_query = """
CREATE TABLE IF NOT EXISTS `group3`.`youtube2` (
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


path = '/Users/sheng/Youtube-Recommendation-System/output'
youtube = pd.concat([pd.read_csv(f, sep=',') for f in glob.glob(path + "/*.csv")],
                      ignore_index=True)
youtube = youtube.where((pd.notnull(youtube)), None)
for i, row in youtube.iterrows():
    sql = "INSERT IGNORE INTO group3.youtube2 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))
    db.commit()
db.close()