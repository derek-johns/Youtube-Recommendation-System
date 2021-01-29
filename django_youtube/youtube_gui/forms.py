from django import forms

class createlist(forms.Form):
    video_id = forms.CharField(max_length=80)