from django import forms

class StoryForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    illustration_url = forms.URLField(required=False)

class PageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    is_ending = forms.BooleanField(required=False)
    ending_label = forms.CharField(required=False)
    illustration_url = forms.URLField(required=False)

class ChoiceForm(forms.Form):
    text = forms.CharField(max_length=255)
    next_page_id = forms.IntegerField()
