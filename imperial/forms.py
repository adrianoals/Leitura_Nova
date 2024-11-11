from django import forms
from .models import Leitura

class LeituraForm(forms.ModelForm):
    valor_leitura = forms.CharField()  # Usamos CharField para capturar o valor como string

    class Meta:
        model = Leitura
        fields = ['apartamento', 'data_leitura', 'valor_leitura', 'foto_relogio']

    def clean_valor_leitura(self):
        valor_leitura = self.cleaned_data.get('valor_leitura', '')

        if ',' not in valor_leitura and '.' not in valor_leitura:
            raise forms.ValidationError('Por favor, insira vírgula para identificar os números em vermelho do seu relógio.')

        valor_leitura = valor_leitura.replace(',', '.')
        # Validar se é um decimal válido com ponto
        try:
            valor_leitura_decimal = forms.DecimalField(max_digits=8, decimal_places=3).clean(valor_leitura)
            return valor_leitura_decimal
        except forms.ValidationError:
            raise forms.ValidationError('Por favor, insira um valor válido para a leitura.')
