from django.urls import path
from tres_coelho.views import tres_coelho, tc_download_photos

urlpatterns = [
    path('tres-coelho', tres_coelho, name='tres_coelho'),
    path('tc-download', tc_download_photos, name='tc_download_photos'),
]


