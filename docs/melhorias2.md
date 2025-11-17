## Controle de Disponibilidade das Páginas de Leitura

### Objetivo
Permitir ativar ou desativar, por condomínio, a página onde moradores enviam leituras. Quando desativado, o formulário deve ficar indisponível e exibir uma mensagem informando que o período está fechado.

### Abordagem
1. **Modelo de Configuração por App**
   - Criar um modelo simples `PortalConfig` em cada app (`tres_coelho`, `imperial`, `alvorada`) com um único campo booleano `is_open` (default `True`).
   - Garantir que exista exatamente um registro por app (pode ser criado automaticamente via `get_or_create` nas views ou sinal/migration).

2. **Admin Django**
   - Registrar `PortalConfig` no admin e habilitar edição direta do campo (ex.: `list_display = ('id', 'is_open')`, `list_editable = ('is_open',)`).
   - Assim, basta marcar/desmarcar no admin para abrir/fechar cada portal.

3. **Views**
   - Em `tres_coelho/views.py`, `imperial/views.py` e `alvorada/views.py`, carregar o `PortalConfig` do app atual.
   - Se `is_open` for `False`, não processar POST e renderizar uma página de aviso, passando `is_open` para o template.
   - Se `True`, seguir com o fluxo atual.

4. **Templates**
   - Incluir um bloco condicional (ex.: `{% if not is_open %}`) para exibir cartão informativo “Período de leituras fechado” e ocultar/desabilitar o formulário.
   - Opcional: manter o formulário mas com todos os campos desabilitados e botão inativo.

5. **Mensagens/UX**
   - Mostrar mensagem clara e eventualmente a data prevista para reabertura (pode ser um campo extra no futuro).
   - Garantir consistência visual nos três templates.

6. **Changelog**
   - Registrar a alteração no histórico sequencial (`docs/changelog/NNNN-controle-portais.md`).

### Próximos Passos
- Implementar o modelo e migrations em cada app.
- Atualizar views/templates e testar o comportamento com porta aberta/fechada.
- Avaliar se precisamos de uma página customizada no futuro para controlar todos os apps em um só lugar.

### Status Atual
- **Tres Coelho**: modelo `PortalConfig`, admin, views e templates já atualizados. Quando `is_open = False`, o formulário é bloqueado e apenas o aviso é exibido.
- **Alvorada**: mesma estrutura implementada (PortalConfig + bloqueio nos templates). Portal já pode ser controlado via admin.
- **Imperial**: estrutura implementada agora; portal pode ser aberto/fechado direto no admin.
