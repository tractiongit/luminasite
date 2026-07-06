import re

with open('clone/index.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find the "Nosso Blog" section (comp-l7z100ri) and remove it
# Also remove the blog-related warmup data
start = html.find('id="comp-l7z100ri"')
if start == -1:
    print('Blog section not found')
    exit(1)

# Go back to find the opening <section tag
sec_start = html.rfind('<section', 0, start)
# Find the closing </section>
sec_end = html.find('</section>', start)
if sec_start != -1 and sec_end != -1:
    sec_end += len('</section>')
    # Also remove the <!--$--> wrapper before the section
    # Look for <!--$--> before sec_start
    wrapper_start = html.rfind('<!--$-->', 0, sec_start)
    if wrapper_start != -1 and wrapper_start > sec_start - 20:
        sec_start = wrapper_start
    
    removed = html[sec_start:sec_end]
    print(f'Removing blog section: {len(removed)} chars')
    html = html[:sec_start] + html[sec_end:]

# Also remove the blog post sections (comp-khv5myfo and related)
# Find "Atendimento de excelência" blog post section
for keyword in ['Atendimento de excel', 'possivel colocar mais de um implante', 'Vamos falar um pouco sobre cuidados']:
    idx = html.find(keyword)
    if idx != -1:
        # Find enclosing section
        s = html.rfind('<section', 0, idx)
        e = html.find('</section>', idx)
        if s != -1 and e != -1:
            e += len('</section>')
            # Check for wrapper
            w = html.rfind('<!--$-->', 0, s)
            if w != -1 and w > s - 20:
                s = w
            print(f'Removing blog post section containing: {keyword[:40]}')
            html = html[:s] + html[e:]

with open('clone/index.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(html)

print('Done! Blog sections removed.')
