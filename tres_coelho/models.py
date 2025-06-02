from django.db import models
from django.core.exceptions import ValidationError
from .supabase_config import supabase, BUCKET_NAME
import os
from datetime import datetime


class Apartamento(models.Model):
    apartamento = models.CharField(max_length=10)

    def __str__(self):
        return self.apartamento


def upload_to_supabase(instance, filename):
    try:
        # Get the current month
        current_month = datetime.now().strftime('%m')
        
        # Create a unique filename
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{instance.apartamento.apartamento}_mes_{current_month}{file_extension}"
        
        # Upload to Supabase
        try:
            # Get the file content
            file_content = instance.foto_relogio.read()
            
            # Determine content type based on file extension
            content_type = 'image/jpeg'  # default
            if file_extension.lower() in ['.png']:
                content_type = 'image/png'
            elif file_extension.lower() in ['.gif']:
                content_type = 'image/gif'
            
            supabase.storage.from_(BUCKET_NAME).upload(
                f"{current_month}/{new_filename}",
                file_content,
                {"content-type": content_type}
            )
            
            # Reset file pointer
            instance.foto_relogio.seek(0)
            
            # Return the public URL
            return f"{current_month}/{new_filename}"
            
        except Exception as e:
            raise ValidationError(f"Erro ao fazer upload da imagem: {str(e)}")
            
    except Exception as e:
        raise ValidationError(f"Erro ao processar a imagem: {str(e)}")


class Leitura(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    valor_leitura = models.DecimalField(max_digits=8, decimal_places=3)
    data_leitura = models.DateField(auto_now_add=True)
    foto_relogio = models.ImageField(upload_to=upload_to_supabase)

    def __str__(self):
        return f"{self.apartamento} - {self.valor_leitura} - {self.data_leitura}"

    def get_foto_url(self):
        if self.foto_relogio:
            try:
                return supabase.storage.from_(BUCKET_NAME).get_public_url(self.foto_relogio.name)
            except:
                return None
        return None

