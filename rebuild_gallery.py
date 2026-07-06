import re
from pathlib import Path

html = open('clone/index.html', encoding='utf-8', errors='ignore').read()

# All gallery images (4 downloaded + 7 new from IMGS)
gallery_images = [
    'assets/86135c_3861485cc1d149cb91e56f284c8c79b4__713d25df.png',
    'assets/86135c_85d9f505c76f4b899fa262a2e38dd873__25805b45.png',
    'assets/86135c_ae554c62089845b19224df57b7030a89__e6c6e715.png',
    'assets/86135c_da2c97d1e8d6497e87e8525ff07f9c56__fe314c6f.png',
    'assets/3316d5b9-5a1e-4622-a9cc-ede24c0ee8ff.jpg',
    'assets/4AB5A1D7-58B1-4B4D-B761-E8F6CBDD560C.JPG',
    'assets/52b76f34-88bd-4a16-ad34-79b084a1a91e.jpg',
    'assets/63c2b089-56bf-44d3-b8fd-0119d7aacec6.jpg',
    'assets/✅.PNG',
    'assets/✅.jpg',
    'assets/✅IMG_8242.HEIC',
]

# Build new gallery HTML - a simple horizontal scrolling gallery
gallery_html = '<div id="pro-gallery-comp-l7av97ly" class="pro-gallery"><div class="pro-gallery-parent-container gallery-slider" style="margin:-2.5px;width:100%;height:384px" role="region"><div id="pro-gallery-container-comp-l7av97ly" class="pro-gallery inline-styles one-row hide-scrollbars slider ltr" style="width:100%;height:386px;display:flex;justify-content:space-between"><div data-hook="gallery-column" id="gallery-horizontal-scroll-comp-l7av97ly" class="gallery-horizontal-scroll gallery-column hide-scrollbars ltr scroll-snap" style="width:100%;height:386px;overflow-y:visible"><div class="gallery-horizontal-scroll-inner" style="display:flex;flex-wrap:nowrap;overflow-x:auto">'

for i, img_src in enumerate(gallery_images):
    gallery_html += f'''<div data-hook="group-view" style="display:flex;flex-wrap:nowrap" aria-hidden="false"><div data-idx="{i}" class="item-link-wrapper" data-hook="item-link-wrapper" tabindex="-1" style="display:block"><div class="gallery-item-container item-container-regular visible clickable zoom-in-on-hover" data-idx="{i}" data-hook="item-container" style="overflow-y:hidden;position:relative;margin:2.5px;width:288px;height:384px;overflow:hidden;opacity:1;display:block" aria-hidden="false"><div data-idx="{i}" class="item-action" tabindex="0" data-hook="item-action" style="width:100%;height:100%;cursor:pointer"><div class="gallery-item-wrapper" data-hook="item-wrapper" style="width:100%;height:100%"><img class="gallery-item-visible gallery-item gallery-item-preloaded" data-hook="gallery-item-image-img" data-idx="{i}" src="{img_src}" loading="lazy" style="width:100%;height:100%;object-fit:cover"/></div></div></div></div>'''

gallery_html += '</div></div></div></div></div>'

# Find and replace the old pro-gallery div
old_start = html.find('<div id="pro-gallery-comp-l7av97ly"')
if old_start == -1:
    print('ERROR: could not find pro-gallery div')
    exit(1)

# Find the matching closing - we need to count divs
depth = 0
i = old_start
while i < len(html):
    if html[i:i+4] == '<div':
        depth += 1
    elif html[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            old_end = i + 6
            break
    i += 1

old_gallery = html[old_start:old_end]
print(f'Old gallery section: {len(old_gallery)} chars')
print(f'New gallery section: {len(gallery_html)} chars')

html = html[:old_start] + gallery_html + html[old_end:]

# Also remove the layout fixer script that references the old gallery
# Find the script tag containing layoutFixerUrl
script_start = html.find('var ele = document.getElementById')
if script_start != -1:
    # Find the <script> tag before it
    s = html.rfind('<script', 0, script_start)
    e = html.find('</script>', script_start)
    if s != -1 and e != -1:
        html = html[:s] + html[e+9:]
        print('Removed layout fixer script')

# Write back
with open('clone/index.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)

print('Done! Gallery rebuilt with', len(gallery_images), 'images')
