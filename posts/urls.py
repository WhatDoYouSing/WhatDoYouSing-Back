from django.urls import path
from .views import *

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view()),
    path("add/", PostView.as_view()),
    path("<int:pk>/", PostView.as_view()),
    path("<int:pk>/likes/", PostLikeView.as_view()),
    path("scrap/<int:pk>/", PostScrapView.as_view()),
]