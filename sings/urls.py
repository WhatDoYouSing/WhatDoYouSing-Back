from django.contrib import admin
from django.urls import path
from .views import *

app_name='sings'      

urlpatterns = [
    path('',HomeCommentsView.as_view()),
    path('latest/',HomeLatestView.as_view()),
    path('likes/',HomeLikesView.as_view()),
    path('recommend/',RecommendView.as_view()),
    path('searchlatest/',SearchLatestView.as_view()),
    path('searchlikes/',SearchLikesView.as_view()),
    path('searchcomments/',SearchCommentsView.as_view()),
    path('emosearchlatest/',SearchEmoLatestView.as_view()),
    path('emosearchlikes/',SearchEmoLikesView.as_view()),
    path('emosearchcomments/',SearchEmoCommentsView.as_view()),
    
    
]