from django.urls import path
from presentation.view.mdData import *

app_name = 'presentation'
urlpatterns = [
    path('init/', UserInputItemView),
    path('main-logic/', MainBusiness),
    path('error-request/', ErrorRequest),
    path('download/<str:result_file_num>/', FileDownload),
]