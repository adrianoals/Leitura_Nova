# from django.shortcuts import render

# def doce_vitta(request):
#     	return render(request, 'doce_vitta/doce_vitta.html')

from django.shortcuts import render, redirect
from .models import Apartamento, Bloco, Leitura
from django.contrib import messages
import datetime

def doce_vitta(request):
    if request.method == 'POST':
        # bloco_id = request.POST.get('bloco')
        apartamento_id = request.POST.get('apartamento')
        valor_leitura = request.POST.get('valor_leitura')
        foto_relogio = request.FILES.get('foto_relogio')

        if not all([apartamento_id, valor_leitura, foto_relogio]):
            messages.error(request, 'Todos os campos são obrigatórios.')
        else:
            apartamento = Apartamento.objects.get(id=apartamento_id)
            Leitura.objects.create(
                apartamento=apartamento,
                valor_leitura=valor_leitura,
                data_leitura=datetime.date.today(),  # Supondo que a data da leitura é sempre o dia atual
                foto_relogio=foto_relogio
            )
            messages.success(request, 'Leitura enviada com sucesso!')
            return redirect('/')

    blocos = Bloco.objects.all()
    apartamentos = Apartamento.objects.all()
    return render(request, 'doce_vitta/doce_vitta.html', {'blocos': blocos, 'apartamentos': apartamentos})
