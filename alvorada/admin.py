from django.contrib import admin
from django.http import HttpResponse
import zipfile
import os
from io import BytesIO
from django.conf import settings
from alvorada.models import Apartamento, Leitura
from alvorada.models import Apartamento, Leitura

# Função para baixar fotos selecionadas como ZIP
@admin.action(description="Baixar fotos selecionadas como ZIP")
def download_photos_as_zip(modeladmin, request, queryset):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for leitura in queryset:
            if leitura.foto_relogio:
                file_path = os.path.join(settings.MEDIA_ROOT, leitura.foto_relogio.name)
                if os.path.exists(file_path):
                    zip_file.write(file_path, os.path.basename(file_path))

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="fotos_selecionadas.zip"'
    return response

# Registro de Apartamento no admin
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento')
    list_display_links = ('id', 'apartamento')

# Registro de Leitura com a ação de baixar fotos
class LeituraAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'data_leitura', 'valor_leitura')
    list_display_links = ('id', 'apartamento', 'data_leitura', 'valor_leitura')
    actions = [download_photos_as_zip]  # Registrando a ação no admin

# Registrando os models no admin
admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Leitura, LeituraAdmin)

