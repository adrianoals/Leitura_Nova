from django.contrib import admin
from doce_vitta.models import Bloco, Apartamento, Leitura

class BlocoAdmin(admin.ModelAdmin):
    list_display = ('id', 'bloco')
    list_display_links = ('id', 'bloco')	

class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'bloco')
    list_display_links = ('id', 'apartamento', 'bloco')	

class LeituraAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'data_leitura', 'valor_leitura')
    list_display_links = ('id', 'apartamento', 'data_leitura', 'valor_leitura')


admin.site.register(Bloco, BlocoAdmin)
admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Leitura, LeituraAdmin)


