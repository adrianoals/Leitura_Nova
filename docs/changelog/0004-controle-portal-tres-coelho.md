# Controle de Portal - Tres Coelho

**Arquivos modificados**
- `tres_coelho/models.py`
- `tres_coelho/migrations/0004_portalconfig.py`
- `tres_coelho/admin.py`
- `tres_coelho/views.py`
- `templates/tres_coelho/tres_coelho_atual.html`
- `templates/tres_coelho/tres_coelho.html`
- `docs/melhorias2.md`

**Descrição detalhada**
- Criamos o modelo `PortalConfig` com flag `is_open` e método helper `get_solo`, além da migration correspondente.
- Registramos o modelo no Django Admin com edição direta do status.
- Atualizamos as views do Tres Coelho para bloquear envios quando o portal estiver fechado e passar `is_portal_open` para os templates.
- Ajustamos os templates atual/legacy para exibir mensagem informativa quando o portal estiver indisponível e esconder o formulário.
- Atualizamos `docs/melhorias2.md` registrando o status atual (Tres Coelho implementado; demais pendentes).

**Passo a passo realizado**
1. Adicionar o modelo e gerar migration.
2. Registrar no admin e ajustar views para usar `PortalConfig`.
3. Atualizar templates com condicionais de exibição.
4. Documentar o status no arquivo de melhorias.

**Critérios de aceitação**
- Administrador consegue ativar/desativar a página do Tres Coelho via Django Admin.
- Moradores visualizam uma mensagem de fechamento quando `is_open = False` e não conseguem enviar o formulário.
- Documentação registra a implementação do condomínio piloto.

**Status final**
- Implementado.
