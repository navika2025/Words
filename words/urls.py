from django.urls import path
from .views import upload_file, download_file

app_name = 'words'

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]
