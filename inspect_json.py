import re
html = open('clone/index.html', encoding='utf-8', errors='ignore').read()
m = re.search(r'wix-essential-viewer-model[\"\']>(.*?)</script>', html, re.S)
if m:
    txt = m.group(1)
    refs = re.findall(r'.{0,120}static\.wixstatic\.com.{0,120}', txt)
    print('found', len(refs))
    for r in refs[:5]:
        print('---')
        print(r)
