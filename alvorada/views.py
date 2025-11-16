from django.shortcuts import render
from alvorada.models import Apartamento, Leitura, PortalConfig
from django.contrib import messages
import datetime
import os
import zipfile
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ValidationError
import pandas as pd
from django.views import View

def alvorada(request):
    config = PortalConfig.get_solo()
    apartamentos = list(Apartamento.objects.all())  # Converte para lista imediatamente
    context = {'apartamentos': apartamentos, 'is_portal_open': config.is_open}

    if not config.is_open:
        if request.method == 'POST':
            messages.warning(request, 'O período de leituras para este condomínio está fechado no momento.')
        return render(request, 'alvorada/alvorada.html', context)

    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento')
        valor_leitura = request.POST.get('valor_leitura')
        # Conversão do valor de leitura para formato decimal (ponto)
        valor_leitura = valor_leitura.replace(',', '.')
        foto_relogio = request.FILES.get('foto_relogio')

        try:
            if not all([apartamento_id, valor_leitura, foto_relogio]):
                raise ValueError('Todos os campos são obrigatórios.')

            apartamento = Apartamento.objects.get(id=apartamento_id)
            Leitura.objects.create(
                apartamento=apartamento,
                valor_leitura=valor_leitura,
                data_leitura=datetime.date.today(),  # Supondo que a data da leitura é sempre o dia atual
                foto_relogio=foto_relogio
            )
            messages.success(request, 'Leitura enviada com sucesso!')
            return render(request, 'alvorada/alvorada.html', context)
        except Exception as e:
            if isinstance(e, ValidationError) and hasattr(e, 'message') and e.message == 'duplicate_upload':
                messages.warning(request, 'Você já enviou a foto deste mês. Não é necessário enviar novamente.')
            elif isinstance(e, ValidationError) and hasattr(e, 'messages') and 'duplicate_upload' in e.messages:
                messages.warning(request, 'Você já enviou a foto deste mês. Não é necessário enviar novamente.')
            elif 'duplicate_upload' in str(e):
                messages.warning(request, 'Você já enviou a foto deste mês. Não é necessário enviar novamente.')
            else:
                messages.error(request, 'Erro ao registrar leitura. Por favor, tente novamente ou contate o suporte.')
            return render(request, 'alvorada/alvorada.html', context)

    return render(request, 'alvorada/alvorada.html', context)


def alvorada_download_photos(request):
    # Caminho base onde as fotos estão armazenadas
    base_directory = os.path.join(settings.MEDIA_ROOT, 'leituras/alvorada')
    
    # Preparar um arquivo zip em memória
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="photos_alvorada.zip"'
    
    # Criar um arquivo ZipFile diretamente na resposta HTTP
    with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as memory_zip:
        # Percorrer diretório e subdiretórios
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                # Construir o caminho completo do arquivo
                file_path = os.path.join(root, file)
                # Adicionar arquivo ao zip
                # Aqui usamos o path relativo para evitar estruturas de diretório absolutas dentro do zip
                memory_zip.write(file_path, os.path.relpath(file_path, base_directory))

    return response


class DownloadExcelView(View):
    def get(self, request):
        # Obter todos os apartamentos da tabela Apartamento
        apartamentos = Apartamento.objects.all().values(
            'apartamento'
        )

        # Obter todas as leituras
        leituras = Leitura.objects.all().values(
            'apartamento__apartamento', 'data_leitura', 'valor_leitura'
        )

        # Criar uma lista de dicionários contendo todos os apartamentos e as leituras (se houver)
        dados = []

        # Iterar sobre todos os apartamentos
        for apartamento in apartamentos:
            # Filtrar as leituras para o apartamento atual
            leituras_apartamento = [leitura for leitura in leituras if 
                                     leitura['apartamento__apartamento'] == apartamento['apartamento']]
            
            if leituras_apartamento:
                # Para cada leitura encontrada, adicionar uma linha com os dados
                for leitura in leituras_apartamento:
                    dados.append({
                        'Apartamento': apartamento['apartamento'],
                        'Data Leitura': leitura['data_leitura'],
                        'Valor Leitura': leitura['valor_leitura']
                    })
            else:
                # Se não houver leituras, adicionar uma linha com os dados do apartamento e leituras vazias
                dados.append({
                    'Apartamento': apartamento['apartamento'],
                    'Data Leitura': None,
                    'Valor Leitura': None
                })

        # Criar o DataFrame
        df = pd.DataFrame(dados)

        # Configurar a resposta HTTP para tipo Excel
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="leituras_alvorada.xlsx"'

        # Salvar o DataFrame no formato Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Apartamentos e Leituras')

        return response

