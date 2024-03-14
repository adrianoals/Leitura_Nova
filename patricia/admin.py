from django.contrib import admin
from patricia.models import Apartamento, Leitura

	
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento')
    list_display_links = ('id', 'apartamento')	

class LeituraAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'data_leitura')
    list_display_links = ('id', 'apartamento', 'data_leitura')


admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Leitura, LeituraAdmin)

