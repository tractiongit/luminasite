import re
html = open('clone/index.html', encoding='utf-8', errors='ignore').read()

for term in ['Recebemos', 'comodidade', 'seguran', 'espa', 'recep', 'cafe', 'café']:
    idx = html.lower().find(term.lower())
    if idx != -1:
        print(f'--- {term} at {idx} ---')
        snippet = html[idx-200:idx+500]
        # remove newlines for readability
        snippet = snippet.replace('\n', ' ')
        print(snippet[:700])
        print()
