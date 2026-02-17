# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.story_list, name='story_list'),
#     path('play/<int:story_id>/', views.play_story, name='play_story'),
#     path('play/<int:story_id>/page/<int:page_id>/', views.play_page, name='play_page'),
#     path('play/<int:story_id>/page/<int:page_id>/choice/<int:choice_id>/', views.make_choice, name='make_choice'),
#     path('stats/', views.stats, name='stats'),
#     path('stats/<int:story_id>/', views.stats, name='story_stats'),
#     path('preview/<int:story_id>/', views.preview_story, name='preview_story'),
#     path('preview/<int:story_id>/page/<int:page_id>/', views.preview_page, name='preview_page'),
#     path('stories/<int:story_id>/delete', views.delete_story, name='delete_story'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('play/<int:story_id>/', views.play_story, name='play_story'),
    path('play/<int:story_id>/page/<int:page_id>/', views.play_page, name='play_page'),
    path('play/<int:story_id>/page/<int:page_id>/choice/<int:choice_id>/', views.make_choice, name='make_choice'),

    path('stats/', views.stats, name='stats'),
    path('stats/<int:story_id>/', views.stats, name='story_stats'),

    path('preview/<int:story_id>/', views.preview_story, name='preview_story'),
    path('preview/<int:story_id>/page/<int:page_id>/', views.preview_page, name='preview_page'),

    path('stories/<int:story_id>/delete', views.delete_story, name='delete_story'),
    path('stories/<int:story_id>/suspend', views.suspend_story, name='suspend_story'),
]
