from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('scrap/', ScrapCollectView.as_view()),
    path('sings/', SingsCollectView.as_view()),
    path('comments/', CommentsCollectView.as_view()),
    path('emotoins/???', EmotionsCollectView.as_view()),
]