import re

html = open('clone/index.html', encoding='utf-8', errors='ignore').read()

# Find section comp-l7av9d6i
m = re.search(r'(<section[^>]+id="comp-l7av9d6i".*?</section>)', html, re.S)
if not m:
    print('section not found')
    exit()
sec = m.group(1)

# Show first 3000 chars of the section
print('Section length:', len(sec))
print()
print(sec[:5000])
