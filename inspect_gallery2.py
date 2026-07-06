import re

html = open('clone/index.html', encoding='utf-8', errors='ignore').read()

m = re.search(r'(<section[^>]+id="comp-l7av9d6i".*?</section>)', html, re.S)
sec = m.group(1)

# Find all img tags
imgs = re.findall(r'<img[^>]+>', sec)
print('img tags:', len(imgs))
for img in imgs[:5]:
    print(img[:400])
    print()

# Find all data-src, srcset, data-uri patterns
data_srcs = re.findall(r'data-src="([^"]+)"', sec)
print('data-src:', len(data_srcs))
for d in data_srcs[:5]:
    print(d[:200])

srcsets = re.findall(r'srcset="([^"]+)"', sec)
print('\nsrcset:', len(srcsets))
for s in srcsets[:3]:
    print(s[:300])

# Find all div with background image style
bgs = re.findall(r'background-image:\s*url\(([^)]+)\)', sec)
print('\nbackground-image:', len(bgs))
for b in bgs[:5]:
    print(b[:200])

# Find all data-uri or data-image references
data_uris = re.findall(r'data-uri="([^"]+)"', sec)
print('\ndata-uri:', len(data_uris))

# Find container IDs
containers = re.findall(r'id="(comp-[^"]+)"', sec)
print('\ncontainer ids:', containers[:20])
