from django import forms
from .models import Apartamento, Leitura

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = ['apartamento', 'bloco']

class LeituraForm(forms.ModelForm):
    class Meta:
        model = Leitura
        fields = ['apartamento', 'data_leitura', 'valor_leitura', 'foto_relogio']
