from tres_coelho.models import Apartamento

# Lista para armazenar os nomes dos apartamentos
apartamentos = []

# Térreo: Apartamentos de 01 a 06
apartamentos.extend([f"Apartamento {i:02d}" for i in range(1, 7)])

# Andares 1 ao 8: Apartamentos 101-112, 201-212, ..., 801-812
for andar in range(1, 9):  # Do 1º ao 8º andar
    apartamentos.extend([f"Apartamento {andar}{i:02d}" for i in range(1, 13)])

# Criar e salvar os apartamentos no banco de dados
for nome in apartamentos:
    apartamento = Apartamento(apartamento=nome)
    apartamento.save()

print("Apartamentos populados com sucesso!")
