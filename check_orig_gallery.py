import re

with open('original_index.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find the gallery section by string search (not regex on whole section)
start = html.find('id="comp-l7av9d6i"')
end = html.find('</section>', start)
sec = html[start:end+10]

# Find all img src
imgs = re.findall(r'src="([^"]+)"', sec)
unique = list(dict.fromkeys(imgs))
print(f'Total: {len(imgs)}, Unique: {len(unique)}')
for u in unique:
    print(u[:250])
