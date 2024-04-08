from django.urls import path
from doce_vitta.views import doce_vitta, doce_vitta_ok, doce_vitta_erro, dv_download_photos

urlpatterns = [
        path('dolce-vita', doce_vitta, name='doce_vitta'), 
        path('ok', doce_vitta_ok, name='doce_vitta_ok'), 
        path('erro', doce_vitta_erro, name='doce_vitta_erro'),
        path('dv-download', dv_download_photos, name='dv_download_photos'),
]



