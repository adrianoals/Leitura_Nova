from django.urls import path
from alvorada.views import alvorada, alvorada_download_photos, ok
urlpatterns = [
        # path('alvorada', alvorada, name='alvorada'), 
        path('dw-alvorada', alvorada_download_photos, name='alvorada_download_photos'),
        path('ok', ok, name='ok'),
]

