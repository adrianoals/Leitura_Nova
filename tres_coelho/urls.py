from django.urls import path
from tres_coelho.views import tres_coelho, tc_download_photos, DownloadExcelView

urlpatterns = [
    # path('3coelhos', tres_coelho, name='tres_coelho'),
    path('tc-download', tc_download_photos, name='tc_download_photos'),
    path('tc-excel/', DownloadExcelView.as_view(), name='tc-excel'),
]


