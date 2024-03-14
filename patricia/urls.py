from django.urls import path
from patricia.views import patricia, download_photos

urlpatterns = [
        path('patricia', patricia, name='patricia'),
    path('patricia-download', download_photos, name='download_photos'),
]


