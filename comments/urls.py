from django.urls import path
from .views import *

app_name = "comments"

urlpatterns = [
    path("<int:post_pk>/", CommentView.as_view()),
    path("del/<int:comment_pk>/", CommentDelView.as_view()),
    path("<int:comment_pk>/likes/", CommentLikeView.as_view()),
    path("<int:comment_pk>/recomments/", RecommentView.as_view()),
    path("del/recomments/<int:recomment_pk>/", RecommentDelView.as_view()),
    path("<int:comment_pk>/recomments/<int:recomment_pk>/relikes/", RecommentLikeView.as_view()),
]