# Clone do site Lúmina / Lara Favrin

Este repositório contém um clone estático do site [https://www.larafavrin.com/](https://www.larafavrin.com/).

## Estrutura

- `clone/` — site clonado (HTML, CSS, JS, imagens e fontes). É a pasta que deve ser servida.
- `download.py` — script que baixa as páginas HTML do site original.
- `localize.py` — script que baixa os assets externos (imagens, CSS, JS, fontes) e reescreve os caminhos para locais.
- `serve.py` — servidor local simples com fallback para SPA (serve `index.html` em rotas desconhecidas).

## Como visualizar localmente

```powershell
python -m http.server 8080 --directory clone
```

Acesse [http://127.0.0.1:8080](http://127.0.0.1:8080) no navegador.

Ou, usando o servidor com fallback SPA:

```powershell
python serve.py
```

## Como atualizar o clone

```powershell
python download.py
python localize.py
```

O site estará em `clone/`.

## Notas

- O site original é feito com Wix. O clone mantém o HTML estático, textos, imagens, cores e fontes originais.
- Alguns recursos externos (como Google Fonts, WhatsApp, Instagram, Analytics) permanecem com links externos, pois não podem ser baixados ou são serviços de terceiros.
- O clone tem 537 arquivos e ~165 MB, incluindo assets de alta resolução.
