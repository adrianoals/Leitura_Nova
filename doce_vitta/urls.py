from django.urls import path
from doce_vitta.views import doce_vitta

urlpatterns = [
        path('', doce_vitta, name='doce_vitta'),  
]



