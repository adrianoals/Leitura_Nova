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
    # Diretório onde as fotos estão armazenadas
    photos_directory = os.path.join(settings.MEDIA_ROOT, 'leituras/dolce_vita')
    
    # Lista de caminhos completos para todas as fotos
    # Filtra apenas arquivos para evitar adicionar diretórios
    photo_paths = [os.path.join(photos_directory, photo) for photo in os.listdir(photos_directory) if os.path.isfile(os.path.join(photos_directory, photo))]
    
    # Configurar um objeto ZipFile em memória
    with zipfile.ZipFile('photos.zip', 'w', zipfile.ZIP_DEFLATED) as memory_zip:
        # Adicionar todas as fotos ao arquivo zip
        for photo_path in photo_paths:
            try:
                memory_zip.write(photo_path, os.path.basename(photo_path))
            except Exception as e:
                return HttpResponse(f"Erro ao adicionar o arquivo ao ZIP: {e}")
    
    # Criar uma resposta HTTP com o arquivo zip
    with open('photos.zip', 'rb') as zip_file:
        response = HttpResponse(zip_file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=photos.zip'

    # Remover o arquivo zip após a criação da resposta
    os.remove('photos.zip')

    return response
