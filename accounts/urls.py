from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('signup/profile/', ProfileChoiceView().as_view()),
    path('login/', LoginView.as_view()),
    path('idconfirm/', DuplicateIDView.as_view()),
    path('update/username/', ChangeUsernameView.as_view()),
    path('update/password/', ChangePasswordView.as_view()),
    path('update/nickname/', ChangeNicknameView.as_view()),
    path('duplicate/',DuplicateIDView.as_view()),
    path('access/', UserAccessView.as_view()),
    path('delete/', UserDeleteView.as_view()),
]