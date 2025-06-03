from django.urls import path
from . import views

urlpatterns = [
    path('3coelhos', views.tres_coelho_atual, name='tres_coelho'),
    path('3coelhos/old', views.tres_coelho, name='tres_coelho_old'),
    path('3coelhos/download', views.tc_download_photos, name='tc_download_photos'),
    path('3coelhos/excel', views.DownloadExcelView.as_view(), name='tc_download_excel'),
]


