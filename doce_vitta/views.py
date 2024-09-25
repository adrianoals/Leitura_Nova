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
        # Obter a lista completa de blocos e unidades (do 001 ao 164 para os blocos 02 e 03)
        blocos = ['01', '02', '03']
        unidades_por_bloco = {
            '01': list(range(1, 155)),  # 154 unidades para bloco 01
            '02': list(range(1, 165)),  # 164 unidades para bloco 02
            '03': list(range(1, 165)),  # 164 unidades para bloco 03
        }

        # Criar uma lista completa de apartamentos no formato [bloco] unidade
        apartamentos_completos = []
        for bloco, unidades in unidades_por_bloco.items():
            for unidade in unidades:
                # Formatar a unidade com 3 dígitos
                unidade_formatada = f'{unidade:03d}'
                apartamentos_completos.append(f'[{bloco}] {unidade_formatada}')

        # Obter as leituras existentes no banco de dados
        leituras_existentes = Leitura.objects.all().values(
            'apartamento__apartamento', 'apartamento__bloco__bloco', 'data_leitura', 'valor_leitura'
        )

        # Criar um dicionário com as leituras formatadas como [bloco] unidade
        leituras_dict = {
            f"[{leitura['apartamento__bloco__bloco']}] {str(leitura['apartamento__apartamento']).zfill(3)}": {
                'data_leitura': leitura['data_leitura'],
                'valor_leitura': leitura['valor_leitura']
            }
            for leitura in leituras_existentes
        }

        # Criar a lista de dados a serem inseridos no DataFrame
        dados = []
        for apartamento in apartamentos_completos:
            leitura = leituras_dict.get(apartamento, {'data_leitura': None, 'valor_leitura': None})
            dados.append({
                'Apartamento': apartamento,
                'Data Leitura': leitura['data_leitura'],
                'Valor Leitura': leitura['valor_leitura']
            })

        # Criar o DataFrame
        df = pd.DataFrame(dados)

        # Configurar a resposta HTTP para tipo Excel
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="leituras_completas_doce_vita.xlsx"'

        # Salvar o DataFrame no formato Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Leituras')

        return response
