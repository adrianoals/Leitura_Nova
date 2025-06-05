from django.urls import path
from alvorada.views import alvorada, alvorada_download_photos
from . import views

urlpatterns = [
        path('alvorada', alvorada, name='alvorada'), 
        path('dw-alvorada', alvorada_download_photos, name='alvorada_download_photos'),
        path('alvorada/excel', views.DownloadExcelView.as_view(), name='download_excel'),
]

