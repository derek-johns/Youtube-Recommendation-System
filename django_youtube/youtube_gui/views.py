from django.shortcuts import render
from django.http import HttpResponse
from .models import thumbnails


def home(request):
    images = thumbnails.objects
    return render(request, 'youtube_gui/home.html', {'images': images})
