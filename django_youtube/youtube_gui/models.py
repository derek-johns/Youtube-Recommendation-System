from django.db import models

class thumbnails(models.Model):
    title = models.CharField(max_length=80)
    image = models.ImageField(upload_to='images/')
    summary = models.CharField(max_length=500)