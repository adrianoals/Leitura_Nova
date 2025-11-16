from django.db import models
from django.utils.timezone import now
from .supabase_config import supabase, BUCKET_NAME
import os
from django.core.exceptions import ValidationError
from .storage import SupabaseStorage


class Apartamento(models.Model):
    apartamento = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apartamento}"


def get_upload_path(instance, filename):
    current_month = now().strftime('%m')
    file_extension = os.path.splitext(filename)[1]
    return f"{current_month}/{instance.apartamento.apartamento}_mes_{current_month}{file_extension}".replace('\\', '/')


class Leitura(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    valor_leitura = models.DecimalField(max_digits=8, decimal_places=3)
    data_leitura = models.DateField(auto_now_add=True)
    foto_relogio = models.ImageField(
        upload_to=get_upload_path,
        storage=SupabaseStorage(),
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.apartamento} - {self.valor_leitura} - {self.data_leitura}"

    def get_foto_url(self):
        if self.foto_relogio:
            try:
                return supabase.storage.from_(BUCKET_NAME).get_public_url(self.foto_relogio.name)
            except:
                return None
        return None


class PortalConfig(models.Model):
    slug = models.CharField(max_length=50, unique=True, default='tres_coelho')
    is_open = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração do Portal"
        verbose_name_plural = "Configurações do Portal"

    def __str__(self):
        status = "Aberto" if self.is_open else "Fechado"
        return f"{self.slug} - {status}"

    @classmethod
    def get_solo(cls):
        config, _ = cls.objects.get_or_create(slug='tres_coelho')
        return config

