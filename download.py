#!/usr/bin/env python3
import os, re, urllib.request, urllib.parse, urllib.error, ssl
from pathlib import Path

BASE_URL = "https://www.larafavrin.com/"
ROOT_DIR = Path(__file__).parent / "clone"
ROOT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

queue = [BASE_URL]
downloaded = set()
errors = []

def safe_path(url):
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)
    if not path or path == "/":
        return ROOT_DIR / "index.html"
    # remove leading slash and query
    local = path.lstrip("/")
    local = re.sub(r"\?.*$", "", local)
    # sanitize Windows reserved chars
    local = re.sub(r"[<>:\"|?*]", "_", local)
    # avoid directory traversal / empty parts
    local = local.replace("../", "_").replace("./", "_")
    # avoid extremely long filenames / paths (Windows MAX_PATH ~ 260)
    MAX_PART = 80
    parts = [p[:MAX_PART] for p in local.split("/")]
    local = "/".join(parts)
    if local.endswith("/"):
        local += "index.html"
    if not Path(local).suffix:
        local = local.rstrip("/") + "/index.html"
    return ROOT_DIR / local

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = resp.read()
        return data
    except Exception as e:
        errors.append(f"{url}: {e}")
        return None

def save(url, data):
    dest = safe_path(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest

def is_internal(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc in ("", "www.larafavrin.com", "larafavrin.com")

def resolve(base, url):
    return urllib.parse.urljoin(base, url).split("#")[0]

def extract_urls(html, base_url):
    urls = set()
    # href and src
    for m in re.finditer(r'(?:href|src)=["\']([^"\']+)["\']', html, re.S):
        u = resolve(base_url, m.group(1))
        if not u.startswith("data:"):
            urls.add(u)
    # srcset
    for m in re.finditer(r'srcset=["\']([^"\']+)["\']', html, re.S):
        for candidate in m.group(1).split(","):
            candidate = candidate.strip().split(" ")[0]
            if candidate and not candidate.startswith("data:"):
                urls.add(resolve(base_url, candidate))
    # url() in CSS
    for m in re.finditer(r'url\(["\']?([^"\')\s]+)["\']?\)', html, re.S):
        u = resolve(base_url, m.group(1))
        if not u.startswith("data:"):
            urls.add(u)
    return urls

def process_page(url):
    if url in downloaded:
        return
    downloaded.add(url)
    print("Downloading page", url)
    data = fetch(url)
    if data is None:
        return
    dest = save(url, data)
    try:
        html = data.decode("utf-8", errors="replace")
    except Exception:
        return
    urls = extract_urls(html, url)
    for u in urls:
        if not is_internal(u):
            continue
        parsed = urllib.parse.urlparse(u)
        # assets: images, css, js, fonts, etc.
        ext = Path(parsed.path.split("?")[0]).suffix.lower()
        ASSET_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".avif", ".css", ".js", ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".mp4", ".webm", ".json", ".xml")
        if ext in ASSET_EXTS:
            if u not in downloaded and len(u) < 500:
                queue.append(u)
        elif ext in (".html", "") or "/post/" in u or "/procedimentos" in u:
            if u not in downloaded and len(u) < 500:
                queue.append(u)

# Start with a few known pages
known_pages = [
    BASE_URL,
    "https://www.larafavrin.com/procedimentos",
    "https://www.larafavrin.com/post/atendimento-de-excel%C3%AAncia-%C3%A9-a-nossa-marca-registrada",
    "https://www.larafavrin.com/post/%C3%A9-poss%C3%ADvel-colocar-mais-de-um-implante-no-mesmo-dia",
    "https://www.larafavrin.com/post/vamos-falar-um-pouco-sobre-cuidados-com-o-seu-aparelho-m%C3%B3vel",
]
for p in known_pages:
    if p not in queue:
        queue.append(p)

while queue:
    url = queue.pop(0)
    process_page(url)

print("Done. Downloaded:", len(downloaded))
if errors:
    print("Errors:")
    for e in errors[:20]:
        print(e)
