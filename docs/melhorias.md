## Restrição de Upload no App Tres Coelho

### Contexto Atual
- O formulário do condomínio Tres Coelho permite que o morador selecione um arquivo existente ao enviar a leitura mensal.
- Em celulares isso abre um seletor genérico, possibilitando anexar fotos antigas e prejudicando a confiabilidade das leituras.
- O backend (`tres_coelho.views`) continua aceitando imagens via `ImageField`, então qualquer arquivo válido é armazenado no bucket Supabase.

### Objetivo
Reduzir a chance de burla pedindo que o usuário tire a foto na hora, priorizando o fluxo mobile (principal canal de acesso).

### Abordagem Inicial (Prioritária)
1. Atualizar o input de arquivo no template `templates/tres_coelho/tres_coelho_atual.html` para usar:
   - `accept="image/*"` para limitar o tipo de arquivo a imagens.
   - `capture="environment"` para instruir navegadores mobile a abrir diretamente a câmera traseira.
2. Ajustar textos do formulário para deixar claro que a foto deve ser feita no momento do envio.
3. Testar em iOS Safari e Android Chrome a fim de confirmar que o seletor abre a câmera; navegadores que não suportam `capture` ainda mostrarão a galeria, mas em geral exibem a opção “Câmera” em destaque.

### Alternativa Mais Rígida (Captura Embutida)
- Utilizar `navigator.mediaDevices.getUserMedia` para abrir a câmera dentro da página, mostrar o preview em um `<video>` e capturar o frame via `<canvas>`/`Blob`. Assim não exibimos o seletor de arquivos nem a galeria padrão.
- **Benefícios**: controla o momento exato da captura, reforça a experiência “foto na hora” e reduz bastante a chance de alguém anexar arquivos existentes.
- **Limitações conhecidas**:
  - Usuários ainda podem apontar a câmera para outra tela/impresso; não existe garantia absoluta contra fraude.
  - Requer HTTPS e suporte a `getUserMedia` (Chrome/Edge/Firefox/Opera/Safari recentes em Android/iOS). Navegadores muito antigos ou restritos podem não funcionar.
  - Em desktops sem câmera ou quando o usuário nega a permissão, precisamos exibir mensagem amigável ou oferecer fallback controlado.
  - Exige tratamento cuidadoso de erros e UX para orientar o morador a liberar o acesso à câmera.
- **Itens técnicos**:
  1. Criar componente JS que inicia/para o stream, permite ao usuário capturar, descartar e recapturar.
  2. Converter o frame para `Blob`/`File` e anexar ao formulário (ex.: usando `FormData` ou `input[type=hidden]` em base64).
  3. Garantir que o backend continue recebendo a imagem via `ImageField` sem alterações estruturais.
  4. Testar em iOS Safari, Android Chrome e navegadores desktop para validar permissões e fluxo.

### Próximos Passos
1. Aplicar a abordagem inicial no app Tres Coelho e validar nos principais dispositivos.
2. Se funcionar bem, replicar para `imperial` e `alvorada`.
3. Monitorar feedback dos moradores; se ainda houver tentativas de burlar, considerar a alternativa com captura embutida e preparar orientações/fallbacks para navegadores não suportados.

