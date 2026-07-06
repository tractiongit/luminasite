import re

orig = open('original_index.html', encoding='utf-8', errors='ignore').read()
clone = open('clone/index.html', encoding='utf-8', errors='ignore').read()

for name, html in [('ORIGINAL', orig), ('CLONE', clone)]:
    print(f'\n=== {name} - section comp-l7hw204i ===')
    m = re.search(r'(<section[^>]+id="comp-l7hw204i".*?</section>)', html, re.S)
    if not m:
        print('section not found')
        continue
    sec = m.group(1)
    imgs = re.findall(r'<img[^>]+>', sec)
    print('img tags:', len(imgs))
    for img in imgs[:5]:
        print(img[:300])
    # count static.wixstatic or assets
    refs = re.findall(r'https://static\.wixstatic\.com/media/[^"\'\s\\)]+', sec)
    print('external wixstatic refs:', len(refs))
    refs2 = re.findall(r'assets/[^"\'\s\\)]+', sec)
    print('local asset refs:', len(refs2))
    # count background image references
    bg = re.findall(r'url\(([^)]+)\)', sec)
    print('url() refs:', len(bg))
    for b in bg[:5]:
        print(b[:200])
