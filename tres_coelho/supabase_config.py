from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Debug das variáveis de ambiente
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos no arquivo .env")

# Inicializar o cliente Supabase usando as variáveis do .env
supabase = create_client(
    supabase_url,
    supabase_key
)

# Nome do bucket no Supabase Storage
BUCKET_NAME = 'leituras-3coelhos' 