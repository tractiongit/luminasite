import re

orig = open('original_index.html', encoding='utf-8', errors='ignore').read()
clone = open('clone/index.html', encoding='utf-8', errors='ignore').read()

for name, html in [('ORIGINAL', orig), ('CLONE', clone)]:
    print(f'\n=== {name} - all sections ===')
    sections = []
    for m in re.finditer(r'<section[^>]+id="([^"]+)".*?</section>', html, re.S):
        sec_id = m.group(1)
        sec = m.group(0)
        h2 = re.search(r'<h2[^>]*>.*?</h2>', sec, re.S)
        title = re.sub(r'<[^>]+>', '', h2.group(0)).strip() if h2 else ''
        imgs = len(re.findall(r'<img[^>]+>', sec))
        bg = len(re.findall(r'url\([^)]+\)', sec))
        wix = len(re.findall(r'wixstatic\.com', sec))
        local = len(re.findall(r'assets/', sec))
        sections.append((sec_id, title, imgs, bg, wix, local))
    for sec_id, title, imgs, bg, wix, local in sections:
        print(f'{sec_id}: title={title[:80]!r}, imgs={imgs}, bg={bg}, wix={wix}, local={local}')
