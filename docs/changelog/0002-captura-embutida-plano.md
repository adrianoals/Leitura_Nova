# Plano de Captura Embutida no Tres Coelho

**Arquivos modificados**
- `docs/melhorias.md`

**Descrição detalhada**
- Documentamos em `docs/melhorias.md` a estratégia de utilizar `navigator.mediaDevices.getUserMedia` como alternativa mais rígida para capturar fotos diretamente no navegador.
- Registramos benefícios, limitações, requisitos técnicos e impacto em compatibilidade/permissões para orientar uma futura implementação.

**Passo a passo realizado**
1. Analisar requisitos adicionais informados pelo usuário sobre impedir o uso de galeria.
2. Detalhar no documento como funcionaria a captura embutida e quais cuidados tomar.
3. Criar este registro sequencial no changelog.

**Critérios de aceitação**
- Documento descreve claramente a alternativa com `getUserMedia` e seus impactos.
- Existe referência no changelog garantindo rastreabilidade da decisão.

**Status final**
- Implementado (documentação atualizada com plano futuro).
