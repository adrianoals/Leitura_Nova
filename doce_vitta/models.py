from django.db import models
from django.utils.timezone import now

class Bloco(models.Model):
    bloco = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.bloco


class Apartamento(models.Model):
    apartamento = models.CharField(max_length=100)
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.apartamento} - {self.bloco.bloco}"

    class Meta:
        unique_together = (('apartamento', 'bloco'),)


def rename_file(instance, filename):
    # Obter o mês atual
    month = now().strftime('%m')
    # Construir o novo nome do arquivo. Você pode ajustar o formato conforme necessário
    new_filename = f"Bloco{instance.apartamento.bloco.bloco}_Ap{instance.apartamento.apartamento}_mes{month}.jpg"
    # Retornar o caminho completo do novo arquivo
    return f"leituras/{month}/{new_filename}"

class Leitura(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    data_leitura = models.DateField()
    valor_leitura = models.DecimalField(max_digits=10, decimal_places=2)
    foto_relogio = models.ImageField(upload_to=rename_file, blank=True, null=True)

    def __str__(self):
        return f"Leitura {self.valor_leitura} - {self.apartamento.apartamento} ({self.data_leitura})"


# class Leitura(models.Model):
#     apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
#     data_leitura = models.DateField()
#     valor_leitura = models.DecimalField(max_digits=10, decimal_places=2)
#     foto_relogio = models.ImageField(upload_to='leituras/%m', blank=True, null=True)

#     def __str__(self):
#         return f"Leitura {self.valor_leitura} - {self.apartamento.apartamento} ({self.data_leitura})"

