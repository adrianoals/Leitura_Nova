from django.urls import path
from imperial.views import imperial, imperial_download_photos, ok
urlpatterns = [
        # path('imperial', imperial, name='imperial'), 
        path('dw-imperial', imperial_download_photos, name='imperial_download_photos'),
        path('ok', ok, name='ok'),
]

