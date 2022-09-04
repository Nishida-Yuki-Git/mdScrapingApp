from django.urls import path
from presentation.view.account import *

app_name = 'presentation'
urlpatterns = [
    path('register/', AuthRegister.as_view()),
    path('mypage/', AuthInfoGetView.as_view()),
    path('login-check/', AuthenticationCheckView.as_view())
]