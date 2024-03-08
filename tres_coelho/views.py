# from django.shortcuts import render

# def tres_coelho(request):
#     	return render(request, 'tres_coelho/tres_coelho.html')


from django.shortcuts import render, redirect
from .models import Apartamento, Leitura
from django.contrib import messages
import datetime

def tres_coelho(request):
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
    apartamentos = Apartamento.objects.all()
    return render(request, 'tres_coelho/tres_coelho.html', {'apartamentos': apartamentos})


# from django.shortcuts import render, redirect
# from .models import Apartamento
# from .forms import LeituraForm  # Certifique-se de importar LeituraForm
# from django.contrib import messages
# import datetime

# def tres_coelho(request):
#     if request.method == 'POST':
#         form = LeituraForm(request.POST, request.FILES)
#         if form.is_valid():
#             leitura = form.save(commit=False)
#             leitura.data_leitura = datetime.date.today()  # Supondo que a data da leitura é sempre o dia atual
#             leitura.save()
#             messages.success(request, 'Leitura enviada com sucesso!')
#             return redirect('/ok')
#         else:
#             # Aqui você pode tratar os erros de validação do formulário
#             messages.error(request, 'Por favor, corrija os erros abaixo.')
#     else:
#         form = LeituraForm()

#     apartamentos = Apartamento.objects.all()
#     return render(request, 'tres_coelho/tres_coelho.html', {'form': form, 'apartamentos': apartamentos})


