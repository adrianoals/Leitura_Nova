from django.shortcuts import render, redirect
from .models import Apartamento, Leitura
from django.contrib import messages
import datetime
import os
import zipfile
from django.http import HttpResponse
from django.conf import settings
from .supabase_config import supabase, BUCKET_NAME
from django.core.exceptions import ValidationError
from django.db import transaction

def tres_coelho(request):
    apartamentos = Apartamento.objects.all()
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                apartamento_id = request.POST.get('apartamento')
                valor_leitura = request.POST.get('valor_leitura')
                foto_relogio = request.FILES.get('foto_relogio')
                
                if not all([apartamento_id, valor_leitura, foto_relogio]):
                    messages.error(request, 'Por favor, preencha todos os campos obrigatórios, incluindo a foto do relógio.')
                    return render(request, 'tres_coelho/tres_coelho.html', {'apartamentos': apartamentos})
                
                apartamento = Apartamento.objects.get(id=apartamento_id)
                
                # Create the Leitura object
                leitura = Leitura.objects.create(
                    apartamento=apartamento,
                    valor_leitura=valor_leitura,
                    foto_relogio=foto_relogio
                )
                
                messages.success(request, 'Leitura registrada com sucesso!')
                return redirect('tres_coelho')
                
        except Apartamento.DoesNotExist:
            messages.error(request, 'Apartamento não encontrado.')
        except Exception as e:
            messages.error(request, f'Erro ao registrar leitura: {str(e)}')
    
    return render(request, 'tres_coelho/tres_coelho.html', {'apartamentos': apartamentos})


def tc_download_photos(request):
    try:
        # Obter todas as leituras com fotos
        leituras = Leitura.objects.exclude(foto_relogio='')
        
        # Criar um arquivo zip em memória
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="photos_tres_coelho.zip"'
        
        # Criar um arquivo ZipFile diretamente na resposta HTTP
        with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as memory_zip:
            for leitura in leituras:
                if leitura.foto_relogio:
                    try:
                        # Obter o arquivo do Supabase Storage
                        file_data = supabase.storage.from_(BUCKET_NAME).download(leitura.foto_relogio.name)
                        # Adicionar ao zip
                        memory_zip.writestr(leitura.foto_relogio.name, file_data)
                    except Exception as e:
                        messages.error(request, f'Erro ao baixar foto {leitura.foto_relogio.name}: {str(e)}')
                        continue

        return response
    except Exception as e:
        messages.error(request, f'Erro ao criar arquivo zip: {str(e)}')
        return redirect('/3coelhos')


import pandas as pd
from django.http import HttpResponse
from django.views import View

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
        response['Content-Disposition'] = 'attachment; filename="leituras_3coelhos.xlsx"'

        # Salvar o DataFrame no formato Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Apartamentos e Leituras')

        return response