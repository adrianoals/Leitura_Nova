from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from django.conf import settings
from .supabase_config import supabase, BUCKET_NAME
import os
from datetime import datetime

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self):
        self.bucket_name = BUCKET_NAME

    def _save(self, name, content):
        try:
            # Lê o conteúdo do arquivo
            file_content = content.read()
            
            # Determina o content type
            content_type = 'image/jpeg'  # default
            if name.lower().endswith('.png'):
                content_type = 'image/png'
            elif name.lower().endswith('.gif'):
                content_type = 'image/gif'

            # Faz o upload para o Supabase
            supabase.storage.from_(self.bucket_name).upload(
                name,
                file_content,
                {"content-type": content_type}
            )

            # Retorna o nome do arquivo (que será armazenado no banco de dados)
            return name
        except Exception as e:
            # Se houver erro de duplicidade
            if hasattr(e, 'args') and any('Duplicate' in str(arg) for arg in e.args):
                from django.core.exceptions import ValidationError
                raise ValidationError("duplicate_upload")
            # Para outros erros
            raise e

    def _open(self, name, mode='rb'):
        try:
            # Obtém o arquivo do Supabase
            response = supabase.storage.from_(self.bucket_name).download(name)
            return ContentFile(response)
        except Exception as e:
            raise e

    def delete(self, name):
        try:
            # Deleta o arquivo do Supabase
            supabase.storage.from_(self.bucket_name).remove([name])
        except Exception as e:
            raise e

    def exists(self, name):
        try:
            # Verifica se o arquivo existe no Supabase
            response = supabase.storage.from_(self.bucket_name).list()
            return name in [item['name'] for item in response]
        except Exception:
            return False

    def url(self, name):
        try:
            # Retorna a URL pública do arquivo
            return supabase.storage.from_(self.bucket_name).get_public_url(name)
        except Exception:
            return None

    def get_available_name(self, name, max_length=None):
        # Se o arquivo já existir, adiciona um timestamp ao nome
        if self.exists(name):
            name_parts = os.path.splitext(name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return f"{name_parts[0]}_{timestamp}{name_parts[1]}"
        return name 