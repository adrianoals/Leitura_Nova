from django.shortcuts import render, redirect
from .models import Apartamento, Bloco, Leitura
from django.contrib import messages
import datetime
import os
import zipfile
from django.http import HttpResponse
from django.conf import settings


def doce_vitta(request):
    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento')
        valor_leitura = request.POST.get('valor_leitura')
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
            return redirect('/ok')
        except Exception as e:
            # Aqui você pode definir uma mensagem de erro com base na exceção
            # e passá-la para a página de erro usando a sessão
            request.session['error_message'] = str(e)  # Usando sessão

    # Se não for uma solicitação POST, exiba a página normalmente
    blocos = Bloco.objects.all()
    apartamentos = Apartamento.objects.all()
    return render(request, 'doce_vitta/doce_vitta.html', {'blocos': blocos, 'apartamentos': apartamentos})

def doce_vitta_ok(request):
    	return render(request, 'doce_vitta/doce_vitta_ok.html')

def doce_vitta_erro(request):
    # Recupera a mensagem de erro da sessão
    error_message = request.session.get('error_message', 'Ocorreu um erro desconhecido.')
    # Limpa a mensagem de erro da sessão após o uso para evitar que seja exibida novamente
    request.session.pop('error_message', None)
    return render(request, 'doce_vitta/doce_vitta_erro.html', {'error_message': error_message})



import os
import zipfile
from django.http import HttpResponse
from django.conf import settings

def dv_download_photos(request):
    # Caminho base onde as fotos estão armazenadas
    base_directory = os.path.join(settings.MEDIA_ROOT, 'leituras/dolce_vita')
    
    # Preparar um arquivo zip em memória
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="photos_dolce_vita.zip"'
    
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

    # Não é necessário remover o arquivo zip, pois ele é criado em memória e enviado diretamente na resposta
    return response

# import pandas as pd
# from django.views import View

# class DownloadExcelView(View):
#     def get(self, request):
#         # Obtendo os dados necessários do modelo Leitura
#         queryset = Leitura.objects.all().values(
#             'apartamento__apartamento', 'apartamento__bloco__bloco', 'data_leitura', 'valor_leitura'
#         )
        
#         # Criando um DataFrame do pandas com os dados
#         df = pd.DataFrame(list(queryset))
        
#         # Configurando a resposta HTTP para tipo Excel
#         response = HttpResponse(
#             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         )
#         response['Content-Disposition'] = 'attachment; filename="leituras_doce_vita.xlsx"'
        
#         # Salvando o DataFrame no formato Excel no buffer de resposta
#         with pd.ExcelWriter(response, engine='openpyxl') as writer:
#             df.to_excel(writer, index=False, sheet_name='Leituras')

#         return response

import pandas as pd
from django.http import HttpResponse
from django.views import View

class DownloadExcelView(View):
    def get(self, request):
        # Obter todos os apartamentos da tabela Apartamento
        apartamentos = Apartamento.objects.all().values(
            'apartamento', 'bloco__bloco'
        )

        # Obter todas as leituras
        leituras = Leitura.objects.all().values(
            'apartamento__apartamento', 'apartamento__bloco__bloco', 'data_leitura', 'valor_leitura'
        )

        # Criar uma lista de dicionários contendo todos os apartamentos e as leituras (se houver)
        dados = []

        # Iterar sobre todos os apartamentos
        for apartamento in apartamentos:
            # Filtrar as leituras para o apartamento atual
            leituras_apartamento = [leitura for leitura in leituras if 
                                     leitura['apartamento__apartamento'] == apartamento['apartamento'] and 
                                     leitura['apartamento__bloco__bloco'] == apartamento['bloco__bloco']]
            
            if leituras_apartamento:
                # Para cada leitura encontrada, adicionar uma linha com os dados
                for leitura in leituras_apartamento:
                    dados.append({
                        'Bloco': apartamento['bloco__bloco'],
                        'Apartamento': apartamento['apartamento'],
                        'Data Leitura': leitura['data_leitura'],
                        'Valor Leitura': leitura['valor_leitura']
                    })
            else:
                # Se não houver leituras, adicionar uma linha com os dados do apartamento e leituras vazias
                dados.append({
                    'Bloco': apartamento['bloco__bloco'],
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
        response['Content-Disposition'] = 'attachment; filename="apartamentos_leituras.xlsx"'

        # Salvar o DataFrame no formato Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Apartamentos e Leituras')

        return response
