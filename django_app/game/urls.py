from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('play/<int:story_id>/', views.play_story, name='play_story'),
    path('choice/<int:page_id>/<int:choice_id>/', views.make_choice, name='make_choice'),
    path('stats/', views.stats, name='stats'),
]
