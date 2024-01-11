from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('profile/', ProfileChoiceView().as_view()),
    path('login/', LoginView.as_view()),
    path('duplicate/', DuplicateIDView.as_view()),
    path('update/password/', ChangePasswordView.as_view()),
    path('update/nickname/', ChangeNicknameView.as_view()),
    path('duplicate/',DuplicateIDView.as_view()),
    path('delete/', UserDeleteView.as_view()),

    path('kakao/', KakaoLoginView.as_view()),
    path('kakao/callback/',KakaoCallbackView.as_view()),
    path('kakao/delete/', KUserDeleteView.as_view()),
]