from django.urls import path
from tres_coelho.views import tres_coelho

urlpatterns = [
        path('', tres_coelho, name='tres_coelho'),
]


