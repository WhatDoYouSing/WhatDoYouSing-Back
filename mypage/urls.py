from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('scrap/', ScrapsCollectView.as_view()),
    path('sings/', PostsCollectView.as_view()),
    path('comments/', CommentsCollectView.as_view()),
    #path('emotoins/???', EmotionsCollectView.as_view()),
]