from django import forms

from .models import Story

class StoryForm(forms.ModelForm): 
    class Meta: 
        model = Story
        fields = ['title', 'description', 'status']

class PageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    is_ending = forms.BooleanField(required=False)
    ending_label = forms.CharField(required=False)
    illustration_url = forms.URLField(required=False)

class ChoiceForm(forms.Form):
    text = forms.CharField(max_length=255)
    next_page_id = forms.IntegerField()
