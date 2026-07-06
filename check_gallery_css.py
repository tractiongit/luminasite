import re

html = open('clone/index.html', encoding='utf-8', errors='ignore').read()

# Find CSS rules related to gallery items
# Look for display:none, visibility:hidden, opacity:0 near gallery
patterns = [
    r'gallery-item[^{]*\{[^}]*display:\s*none[^}]*\}',
    r'gallery-item[^{]*\{[^}]*visibility:\s*hidden[^}]*\}',
    r'gallery-item[^{]*\{[^}]*opacity:\s*0[^}]*\}',
    r'comp-l7av9d6i[^{]*\{[^}]*display:\s*none[^}]*\}',
    r'comp-l7av97ly[^{]*\{[^}]*\}',
    r'gallery-item-visible[^{]*\{[^}]*\}',
    r'gallery-item-preloaded[^{]*\{[^}]*\}',
]

for p in patterns:
    matches = re.findall(p, html, re.I)
    if matches:
        print(f'--- {p[:50]} ---')
        for m in matches[:3]:
            print(m[:300])
        print()

# Also check for the gallery container dimensions
m = re.search(r'comp-l7av97ly[^{]*\{([^}]+)\}', html)
if m:
    print('comp-l7av97ly style:', m.group(1)[:300])

# Check for height:0 or max-height:0
height_patterns = re.findall(r'[^{]*(gallery|comp-l7av9)[^{]*\{[^}]*height:\s*0[^}]*\}', html, re.I)
print('height:0 rules:', len(height_patterns))

# Check for the pro-gallery component
pg = re.findall(r'<[^>]+pro-gallery[^>]*>', html, re.I)
print('\npro-gallery elements:', len(pg))
for p in pg[:3]:
    print(p[:300])
