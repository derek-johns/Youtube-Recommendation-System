from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Youtube
from .forms import createlist
from .ml import get_recommendations
import pandas as pd
from django.db.models import Q


def home(response):
    images = Youtube.objects
    return render(response, 'youtube_gui/home.html', {'images': images})

def mlpage(response, video_id):
    df = get_recommendations(video_id)
    vid_list = df.video_id.tolist()
    images = Youtube.objects.filter(
        Q(video_id=vid_list[0]) | Q(video_id=vid_list[1]) | Q(video_id=vid_list[2]) | Q(video_id=vid_list[3]) | Q(video_id=vid_list[4]) |
        Q(video_id=vid_list[5]) | Q(video_id=vid_list[6]) | Q(video_id=vid_list[7]) | Q(video_id=vid_list[8]) | Q(video_id=vid_list[9]))
    return render(response, "youtube_gui/mlpage.html", {"video_id":video_id, 'images': images})
