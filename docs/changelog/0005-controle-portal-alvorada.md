# Controle de Portal - Alvorada

**Arquivos modificados**
- `alvorada/models.py`
- `alvorada/migrations/0004_portalconfig.py`
- `alvorada/admin.py`
- `alvorada/views.py`
- `templates/alvorada/alvorada.html`
- `docs/melhorias2.md`

**Descrição detalhada**
- Adicionamos o modelo `PortalConfig` no app Alvorada, com método helper para garantir registro único.
- Registramos o modelo no Django Admin para permitir ativar/desativar o portal rapidamente.
- As views agora consultam `PortalConfig` antes de aceitar POSTs e passam `is_portal_open` aos templates.
- O template principal exibe um aviso quando o portal está fechado e oculta o formulário.
- Atualizamos o documento de melhorias registrando o novo status do Alvorada.

**Passo a passo realizado**
1. Criar modelo e migration.
2. Registrar no admin e ajustar views/contexto.
3. Atualizar template com condicionais.
4. Documentar no arquivo de melhorias e registrar este changelog.

**Critérios de aceitação**
- Administrador consegue fechar/abrir o portal Alvorada via Django Admin.
- Moradores veem mensagem de fechamento e não conseguem enviar quando `is_open = False`.
- Documentação reflete o status atualizado.

**Status final**
- Implementado.
