import re

clone = open('clone/index.html', encoding='utf-8', errors='ignore').read()

m = re.search(r'(<section[^>]+id="comp-l7av9d6i".*?</section>)', clone, re.S)
sec = m.group(1)

# Find local asset references
local = re.findall(r'assets/[^"\'\s\\)]+', sec)
print('local assets in hero section:', len(local))
for u in local[:20]:
    print(u)

# Find external wixstatic refs
external = re.findall(r'https://static\.wixstatic\.com/media/[^"\'\s\\)]+', sec)
print('\nexternal wixstatic in hero section:', len(external))
for u in external[:20]:
    print(u)
