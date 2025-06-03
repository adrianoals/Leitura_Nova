from django.db import models
from django.utils.timezone import now
from .supabase_config import supabase, BUCKET_NAME
import os
from django.core.exceptions import ValidationError


class Apartamento(models.Model):
    apartamento = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apartamento}"


def upload_to_supabase(instance, filename):
    try:
        current_month = now().strftime('%m')
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{instance.apartamento.apartamento}_mes_{current_month}{file_extension}"
        try:
            file_content = instance.foto_relogio.read()
            content_type = 'image/jpeg'
            if file_extension.lower() in ['.png']:
                content_type = 'image/png'
            elif file_extension.lower() in ['.gif']:
                content_type = 'image/gif'
            supabase.storage.from_(BUCKET_NAME).upload(
                f"{current_month}/{new_filename}",
                file_content,
                {"content-type": content_type}
            )
            instance.foto_relogio.seek(0)
            return f"{current_month}/{new_filename}"
        except Exception as e:
            raise ValidationError(f"Erro ao fazer upload da imagem: {str(e)}")
    except Exception as e:
        raise ValidationError(f"Erro ao processar a imagem: {str(e)}")

class Leitura(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    data_leitura = models.DateField()
    valor_leitura = models.DecimalField(max_digits=8, decimal_places=3)
    foto_relogio = models.ImageField(upload_to=upload_to_supabase, blank=True, null=True)

    def __str__(self):
        return f"Leitura {self.valor_leitura} - {self.apartamento.apartamento} ({self.data_leitura})"
