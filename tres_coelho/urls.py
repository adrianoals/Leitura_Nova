from django.urls import path
from tres_coelho.views import tres_coelho, download_photos

urlpatterns = [
    path('tres-coelho', tres_coelho, name='tres_coelho'),
    path('tres-coelho-download', download_photos, name='download_photos'),
]


