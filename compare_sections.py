import re

orig = open('original_index.html', encoding='utf-8', errors='ignore').read()
clone = open('clone/index.html', encoding='utf-8', errors='ignore').read()

# List image URLs in original vs clone
orig_imgs = set(re.findall(r'https://static\.wixstatic\.com/media/[^"\'\s\\)]+', orig))
clone_imgs = set(re.findall(r'assets/[^"\'\s\\)]+', clone))

print('Original static.wixstatic.com image URLs:', len(orig_imgs))
for u in sorted(orig_imgs)[:30]:
    print(u)
print()
print('Clone local assets:', len(clone_imgs))
for u in sorted(clone_imgs)[:30]:
    print(u)
print()

# Find sections by image id patterns
for term in ['espaço', 'recepção', 'consultório', 'cafe', 'café', 'sala', 'espera']:
    o = orig.lower().find(term.lower())
    c = clone.lower().find(term.lower())
    print(f'{term}: orig={o}, clone={c}')
