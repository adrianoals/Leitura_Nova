# from django.shortcuts import render

# def doce_vitta(request):
#     	return render(request, 'doce_vitta/doce_vitta.html')

# from django.shortcuts import render, redirect
# from .models import Apartamento, Bloco, Leitura
# from django.contrib import messages
# import datetime

# def doce_vitta(request):
#     if request.method == 'POST':
#         # bloco_id = request.POST.get('bloco')
#         apartamento_id = request.POST.get('apartamento')
#         valor_leitura = request.POST.get('valor_leitura')
#         foto_relogio = request.FILES.get('foto_relogio')

#         if not all([apartamento_id, valor_leitura, foto_relogio]):
#             messages.error(request, 'Todos os campos são obrigatórios.')
#         else:
#             apartamento = Apartamento.objects.get(id=apartamento_id)
#             Leitura.objects.create(
#                 apartamento=apartamento,
#                 valor_leitura=valor_leitura,
#                 data_leitura=datetime.date.today(),  # Supondo que a data da leitura é sempre o dia atual
#                 foto_relogio=foto_relogio
#             )
#             messages.success(request, 'Leitura enviada com sucesso!')
#             return redirect('/ok')

#     blocos = Bloco.objects.all()
#     apartamentos = Apartamento.objects.all()
#     return render(request, 'doce_vitta/doce_vitta.html', {'blocos': blocos, 'apartamentos': apartamentos})

from django.shortcuts import render, redirect
from .models import Apartamento, Bloco, Leitura
from django.contrib import messages
import datetime
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# def doce_vitta(request):
#     if request.method == 'POST':
#         apartamento_id = request.POST.get('apartamento')
#         valor_leitura = request.POST.get('valor_leitura')
#         foto_relogio = request.FILES.get('foto_relogio')

#         try:
#             if not all([apartamento_id, valor_leitura, foto_relogio]):
#                 raise ValueError('Todos os campos são obrigatórios.')

#             try:
#                 apartamento = Apartamento.objects.get(id=apartamento_id)
#             except ObjectDoesNotExist:
#                 raise ValueError('Apartamento selecionado não existe.')

#             # Aqui você pode adicionar outras validações, como formato do valor_leitura

#             Leitura.objects.create(
#                 apartamento=apartamento,
#                 valor_leitura=valor_leitura,
#                 data_leitura=datetime.date.today(),
#                 foto_relogio=foto_relogio
#             )
#             messages.success(request, 'Leitura enviada com sucesso!')
#         except ValueError as e:
#             messages.error(request, str(e))
#         except Exception as e:  # Captura outros erros genéricos
#             messages.error(request, 'Ocorreu um erro ao processar sua solicitação.\nPor favor, tente novamente.')

#         return redirect('/ok')  # Ou redirecione para outra página conforme necessário

#     blocos = Bloco.objects.all()
#     apartamentos = Apartamento.objects.all()
#     return render(request, 'doce_vitta/doce_vitta.html', {'blocos': blocos, 'apartamentos': apartamentos})

from django.shortcuts import render, redirect
from .models import Apartamento, Bloco, Leitura
from django.contrib import messages
import datetime

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
            return redirect('/erro')  # Substitua '/erro' pelo caminho para sua página de erro

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
