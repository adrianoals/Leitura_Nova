from django.urls import path
from alvorada.views import imperial, imperial_download_photos
urlpatterns = [
        path('imperial', imperial, name='imperial'), 
        path('dv-imperial', imperial_download_photos, name='imperial_download_photos'),
]

