# LuminaSite — orientações

- Site estático: https://luminaodonto.com.br/
- Repositório: https://github.com/tractiongit/luminasite
- Materiais e contexto: `C:\Users\User\Documents\TRT - Lumina\AGENTS.md`.
- Entrada: `index.html` na raiz; recursos em `assets/`; comportamento em `script.js`.
- O HTML contém CSS inline que difere de `styles.css`. Não executar automaticamente `inline_css.py`: acrescenta outro bloco e pode reintroduzir estilos antigos.
- Tailwind está compilado. Verificar disponibilidade de novas classes ou usar CSS específico.
- Preservar layout, links, rastreamento e conteúdo fora do escopo.
- Conferir git status e preservar alterações existentes antes de editar.
- Scripts antigos de download/localização e clone_backup são históricos; não executá-los para atualizar conteúdo.
- Preview: `python -m http.server 8080 --bind 127.0.0.1` nesta pasta.
- Validar imagens, caminhos locais e apresentação responsiva após mudanças visuais.
- Publicação ainda não identificada. Não afirmar que a versão local está no ar sem verificar.
- Nunca registrar tokens, senhas ou remotes com credenciais.
