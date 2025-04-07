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
    return f"leituras/alvorada/{month}/{new_filename}"

class Leitura(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    data_leitura = models.DateField()
    valor_leitura = models.DecimalField(max_digits=8, decimal_places=3)
    foto_relogio = models.ImageField(upload_to=rename_file, blank=True, null=True)

    def __str__(self):
        return f"Leitura {self.valor_leitura} - {self.apartamento.apartamento} ({self.data_leitura})"
