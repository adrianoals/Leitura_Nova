# Controle de Portal - Imperial

**Arquivos modificados**
- `imperial/models.py`
- `imperial/migrations/0004_portalconfig.py`
- `imperial/admin.py`
- `imperial/views.py`
- `templates/imperial/imperial.html`
- `docs/melhorias2.md`

**Descrição detalhada**
- Adicionamos o modelo `PortalConfig` no app Imperial com flag `is_open` e método helper para garantir registro único.
- Registramos o modelo no Django Admin permitindo ativar/desativar o portal diretamente.
- A view principal agora consulta `PortalConfig` antes de processar POSTs e envia `is_portal_open` ao template.
- O template exibe aviso quando o portal está fechado e oculta o formulário.
- Atualizamos o documento de melhorias para refletir que Imperial também possui o controle.

**Passo a passo realizado**
1. Criar modelo + migration e registrar no admin.
2. Ajustar view para usar o flag e bloquear envios quando necessário.
3. Atualizar template com mensagem condicional.
4. Atualizar documentação e registrar este changelog.

**Critérios de aceitação**
- Admin consegue habilitar/desabilitar o portal Imperial via painel.
- Moradores visualizam mensagem de fechamento quando `is_open = False` e não conseguem enviar leituras.
- Documentação reflete o estado atualizado.

**Status final**
- Implementado.
