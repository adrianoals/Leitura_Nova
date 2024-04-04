from django.urls import path
from tres_coelho.views import tc_download_photos

urlpatterns = [
    # path('tres-coelho', tres_coelho, name='tres_coelho'),
    path('tres-coelho-download', tc_download_photos, name='tc_download_photos'),
]


