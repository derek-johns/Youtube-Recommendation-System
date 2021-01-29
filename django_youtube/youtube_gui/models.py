from django.db import models

class thumbnails(models.Model):
    title = models.CharField(max_length=80)
    image = models.ImageField(upload_to='images/')
    summary = models.CharField(max_length=500)

class Youtube(models.Model):
    video_id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    publishedat = models.CharField(db_column='publishedAt', max_length=45, blank=True, null=True)  # Field name made lowercase.
    channelid = models.CharField(db_column='channelId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    channeltitle = models.CharField(db_column='channelTitle', max_length=60, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    trending_date = models.DateTimeField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    thumbnail_link = models.CharField(max_length=100, blank=True, null=True)
    comments_disabled = models.IntegerField(blank=True, null=True)
    ratings_disabled = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'youtube'


class Youtube3(models.Model):
    video_id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    publishedat = models.CharField(db_column='publishedAt', max_length=45, blank=True, null=True)  # Field name made lowercase.
    channelid = models.CharField(db_column='channelId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    channeltitle = models.CharField(db_column='channelTitle', max_length=60, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    trending_date = models.DateTimeField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    comment_count = models.IntegerField(blank=True, null=True)
    thumbnail_link = models.CharField(max_length=100, blank=True, null=True)
    comments_disabled = models.CharField(max_length=45, blank=True, null=True)
    ratings_disabled = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        db_table = 'youtube3'


class YoutubeCategory(models.Model):
    categoryid = models.IntegerField(db_column='categoryId', primary_key=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='category_Name', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'youtube_category'