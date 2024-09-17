from django.contrib import admin
from doce_vitta.models import Bloco, Apartamento, Leitura
from django.http import HttpResponse
import zipfile
import os
from io import BytesIO
from django.conf import settings

@admin.action(description="Baixar fotos selecionadas como ZIP")
def download_photos_as_zip(modeladmin, request, queryset):
    # Criar um arquivo ZIP em memória
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for leitura in queryset:
            if leitura.foto_relogio:  # Supondo que foto_relogio é o campo da imagem no modelo Leitura
                # Caminho completo da foto
                file_path = os.path.join(settings.MEDIA_ROOT, leitura.foto_relogio.name)  # Usando settings.MEDIA_ROOT e nome do arquivo
                if os.path.exists(file_path):
                    # Adicionar ao ZIP com o nome da foto, baseando-se na lógica do caminho
                    zip_file.write(file_path, os.path.basename(file_path))
    
    # Enviar o arquivo ZIP como resposta HTTP
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="fotos_selecionadas.zip"'
    return response

class BlocoAdmin(admin.ModelAdmin):
    list_display = ('id', 'bloco')
    list_display_links = ('id', 'bloco')

class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'bloco')
    list_display_links = ('id', 'apartamento', 'bloco')

class LeituraAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'data_leitura', 'valor_leitura')
    list_display_links = ('id', 'apartamento', 'data_leitura', 'valor_leitura')
    actions = [download_photos_as_zip]  # Adicionando a ação de download de fotos

admin.site.register(Bloco, BlocoAdmin)
admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Leitura, LeituraAdmin)



# from django.contrib import admin
# from doce_vitta.models import Bloco, Apartamento, Leitura

# class BlocoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'bloco')
#     list_display_links = ('id', 'bloco')	

# class ApartamentoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'apartamento', 'bloco')
#     list_display_links = ('id', 'apartamento', 'bloco')	

# class LeituraAdmin(admin.ModelAdmin):
#     list_display = ('id', 'apartamento', 'data_leitura', 'valor_leitura')
#     list_display_links = ('id', 'apartamento', 'data_leitura', 'valor_leitura')


# admin.site.register(Bloco, BlocoAdmin)
# admin.site.register(Apartamento, ApartamentoAdmin)
# admin.site.register(Leitura, LeituraAdmin)


