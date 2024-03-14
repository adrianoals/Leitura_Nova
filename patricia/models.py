from django.db import models
from django.utils.timezone import now


class Apartamento(models.Model):
    apartamento = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apartamento}"


def rename_file(instance, filename):
    # Obter o mês atual
    month = now().strftime('%m')
    # Construir o novo nome do arquivo. Você pode ajustar o formato conforme necessário
    new_filename = f"{instance.apartamento.apartamento}_mês_{month}.jpg"
    # Retornar o caminho completo do novo arquivo
    return f"leituras/patricia/{month}/{new_filename}"

class Leitura(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    data_leitura = models.DateField()
    valor_leitura_cozinha = models.DecimalField(max_digits=8, decimal_places=3)
    valor_leitura_banheiro = models.DecimalField(max_digits=8, decimal_places=3)
    foto_relogio_cozinha = models.ImageField(upload_to=rename_file, blank=True, null=True)
    foto_relogio_banheiro = models.ImageField(upload_to=rename_file, blank=True, null=True)

    def __str__(self):
        return f"Leitura cozinha {self.valor_leitura_cozinha} - Leitura banheiro {self.valor_leitura_banheiro} {self.apartamento.apartamento} ({self.data_leitura})"

