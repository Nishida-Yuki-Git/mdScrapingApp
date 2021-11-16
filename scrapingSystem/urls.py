from django.urls import path
from . import views

app_name = 'scrapingSystem'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('results/', views.results, name='results'),
    path('create/', views.create_account, name='create_account'),
    path('login/', views.account_login, name='login'),
    path('logout/', views.account_logout, name='logout'),
    path('download/<int:result_file_num>/', views.download, name='download')
]