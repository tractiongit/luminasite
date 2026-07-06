import re

orig = open('original_index.html', encoding='utf-8', errors='ignore').read()
clone = open('clone/index.html', encoding='utf-8', errors='ignore').read()

# Find all section ids and headings in order
for name, html in [('ORIGINAL', orig), ('CLONE', clone)]:
    print(f'\n=== {name} sections ===')
    # Find h2 text
    for m in re.finditer(r'<h2[^>]*>.*?</h2>', html, re.S):
        txt = re.sub(r'<[^>]+>', '', m.group(0))
        if txt.strip():
            print(txt.strip()[:120])
    print('---')
    # Find section ids with comp-
    ids = re.findall(r'<section[^>]+id="(comp-l[^"]+)"', html)
    print('section ids:', ids[:20])
