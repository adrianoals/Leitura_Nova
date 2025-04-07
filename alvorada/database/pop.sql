-- python manage.py shell

from alvorada.models import Apartamento

# Lista de apartamentos fornecida

lista_apartamentos = [
    'Apartamento 11', 'Apartamento 12', 'Apartamento 13', 'Apartamento 14', 'Apartamento 21', 'Apartamento 22', 'Apartamento 23', 'Apartamento 24', 'Apartamento 31', 'Apartamento 32', 'Apartamento 33', 'Apartamento 34', 'Apartamento 41', 'Apartamento 42', 'Apartamento 43', 'Apartamento 44', 'Apartamento 51', 'Apartamento 52', 'Apartamento 53', 'Apartamento 54', 'Apartamento 61', 'Apartamento 62', 'Apartamento 63', 'Apartamento 64', 'Apartamento 71', 'Apartamento 72', 'Apartamento 73', 'Apartamento 74', 'Apartamento 81', 'Apartamento 82', 'Apartamento 83', 'Apartamento 84', ]


# Iterate over the list of apartment strings and create Apartamento instances
for apartamento in lista_apartamentos:
    apartamento, created = Apartamento.objects.get_or_create(apartamento=apartamento)
    if created:
        print(f'Apartamento {apartamento} criado com sucesso.')
    else:
        print(f'Apartamento {apartamento} já existe.')
