```
# Leitura Nova

**Leitura Nova** é um projeto desenvolvido para a empresa Leitura Nova com o objetivo de gerenciar as leituras de hidrômetros de água ou medidores de gás localizados dentro dos apartamentos. O sistema permite que os usuários, ao acessarem o link do projeto disponível online, selecionem sua unidade e enviem uma foto do seu medidor. Isso facilita o controle do consumo mensal dos condomínios pela empresa Leitura Nova, que pode monitorar o consumo de forma eficiente.

## Funcionalidades

- Seleção de unidade: o usuário pode escolher sua unidade no sistema.
- Upload de foto: o usuário envia uma foto do medidor (hidrômetro de água ou medidor de gás).
- Gestão do consumo: a empresa Leitura Nova pode gerenciar o consumo mensal dos condomínios de forma centralizada.

## Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Python**: Linguagem de programação principal.
- **Django**: Framework utilizado para o desenvolvimento do backend.
- **HTML**, **CSS** e **Bootstrap**: Utilizados para o desenvolvimento do frontend responsivo e interativo.
- **JavaScript**: Utilizado para interações dinâmicas e validação no frontend.
- **AWS EC2**: O projeto está hospedado em uma instância EC2 da AWS, garantindo disponibilidade e escalabilidade.

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd leitura-nova
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurações de Ambiente

Crie um arquivo `.env` na raiz do projeto e configure suas variáveis de ambiente, como as chaves de acesso à AWS, configurações de banco de dados e outras variáveis sensíveis.

### 5. Migrações do Banco de Dados

Execute as migrações do banco de dados para configurar as tabelas necessárias:

```bash
python manage.py migrate
```

### 6. Executar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse o projeto no navegador através do link `http://localhost:8000`.

## Hospedagem

O projeto está hospedado em uma instância **AWS EC2**, oferecendo alta disponibilidade e escalabilidade. A configuração do servidor inclui:

- **NGINX** como servidor web.
- **Gunicorn** para o servidor de aplicação Python.
- Banco de dados configurado conforme a necessidade do projeto.

## Contribuição

Se você deseja contribuir para o projeto, siga as etapas:

1. Faça um fork do projeto.
2. Crie uma nova branch (`git checkout -b minha-branch`).
3. Commit suas alterações (`git commit -m 'Adicionar nova funcionalidade'`).
4. Faça o push para a branch (`git push origin minha-branch`).
5. Abra um Pull Request.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

---

**Leitura Nova** - Facilitando a gestão de consumo em condomínios.
```
