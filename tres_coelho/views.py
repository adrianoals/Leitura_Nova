# from django.shortcuts import render

# def tres_coelho(request):
#     	return render(request, 'tres_coelho/tres_coelho.html')

from django.shortcuts import render, redirect
from .models import Apartamento, Leitura
from django.contrib import messages
import datetime
import os
import zipfile
from django.http import HttpResponse
from django.conf import settings

def tc_download_photos(request):
    # Diretório onde as fotos estão armazenadas
    photos_directory = os.path.join(settings.MEDIA_ROOT, 'leituras/tres_coelho/03')
    
    # Lista de caminhos completos para todas as fotos
    photo_paths = [os.path.join(photos_directory, photo) for photo in os.listdir(photos_directory)]
    
    # Configurar um objeto ZipFile em memória
    memory_zip = zipfile.ZipFile('photos.zip', 'w', zipfile.ZIP_DEFLATED)

    # Adicionar todas as fotos ao arquivo zip
    for photo_path in photo_paths:
        memory_zip.write(photo_path, os.path.basename(photo_path))

    # Fechar o arquivo zip
    memory_zip.close()

    # Criar uma resposta HTTP com o arquivo zip em memória
    response = HttpResponse(open('photos.zip', 'rb'), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=photos.zip'

    # Remover o arquivo zip em memória após o envio
    os.remove('photos.zip')

    return response

def dv_download_photos(request):
    # Caminho base onde as fotos estão armazenadas
    base_directory = os.path.join(settings.MEDIA_ROOT, 'leituras/tres_coelho')
    
    # Preparar um arquivo zip em memória
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="photos_tres_coelho.zip"'
    
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