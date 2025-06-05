from django.urls import path
from imperial.views import imperial, imperial_download_photos
from . import views

urlpatterns = [
        path('imperial', imperial, name='imperial'), 
        path('dw-imperial', imperial_download_photos, name='imperial_download_photos'),
        path('imperial/excel', views.DownloadExcelView.as_view(), name='download_excel'),
]

