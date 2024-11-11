from imperial.models import Apartamento

# Lista de apartamentos
casas = [f"Casa {i:02d}" for i in range(1, 17)]  # Gera "Casa 01" até "Casa 16"

# Criar e salvar os objetos no banco de dados
for casa in casas:
    apartamento = Apartamento(apartamento=casa)
    apartamento.save()

print("Apartamentos populados com sucesso!")
