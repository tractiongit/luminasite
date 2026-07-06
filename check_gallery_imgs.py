import re, json
from pathlib import Path

html = open('clone/index.html', encoding='utf-8', errors='ignore').read()

m = re.search(r'(<section[^>]+id="comp-l7av9d6i".*?</section>)', html, re.S)
sec = m.group(1)

# Find all img src in gallery
imgs = re.findall(r'src="(assets/[^"]+)"', sec)
unique = list(dict.fromkeys(imgs))
print(f'Total img refs: {len(imgs)}, unique: {len(unique)}')

for u in unique:
    p = Path('clone') / u
    exists = p.exists()
    size = p.stat().st_size if exists else 0
    print(f'  {u}  exists={exists}  size={size}')
