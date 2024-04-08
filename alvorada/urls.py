from django.urls import path
from alvorada.views import alvorada, alvorada_download_photos

urlpatterns = [
        path('alvorada', alvorada, name='doce_vitta'), 
        path('alvorda', alvorada_download_photos, name='alvorada_download_photos'),
]

