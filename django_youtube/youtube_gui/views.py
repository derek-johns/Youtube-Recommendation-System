from django.shortcuts import render
from django.http import HttpResponse
from .models import Youtube


def home(request):
    images = Youtube.objects
    return render(request, 'youtube_gui/home.html', {'images': images})
