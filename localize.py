#!/usr/bin/env python3
"""Download external assets referenced in clone/ and rewrite URLs to local paths."""
import os, re, hashlib, urllib.request, urllib.parse, ssl, json
from pathlib import Path

ROOT = Path(__file__).parent / "clone"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

map_file = ROOT / "assets" / "urlmap.json"
url_map = {}
if map_file.exists():
    try:
        url_map = json.loads(map_file.read_text(encoding="utf-8"))
    except Exception:
        url_map = {}

errors = []

def asset_local_name(url):
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)
    base = Path(path).name or "asset"
    base = re.sub(r"[<>:\"|?*]", "_", base)
    ext = Path(base).suffix.lower()
    if not ext or len(ext) > 6:
        # try to infer from query or default
        ext = ".bin"
    h = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
    safe = re.sub(r"[^\w\-\.]", "_", Path(base).stem)[:40]
    return f"{safe}_{h}{ext}"

def fetch(url, max_bytes=100*1024*1024):
    if url in url_map:
        return url_map[url]
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
            data = resp.read(max_bytes+1)
        if len(data) > max_bytes:
            errors.append(f"Too big: {url}")
            return None
        return data
    except Exception as e:
        errors.append(f"{url}: {e}")
        return None

def rewrite_url(url, file_path):
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return url
    if parsed.scheme not in ("http", "https"):
        return url
    # skip non-asset external domains (e.g. whatsapp, instagram, youtube, google fonts api)
    host = parsed.netloc.lower()
    if any(x in host for x in ["api.whatsapp.com", "instagram.com", "facebook.com", "youtube.com", "google.com", "googletagmanager.com", "google-analytics.com", "doubleclick.net", "connect.facebook.net"]):
        return url
    # Determine if asset by extension or host
    path = urllib.parse.unquote(parsed.path)
    ext = Path(path.split("?")[0]).suffix.lower()
    asset_hosts = ["static.wixstatic.com", "static.parastorage.com", "siteassets.parastorage.com", "pages.parastorage.com", "viewer-apps.parastorage.com", "viewer-assets.parastorage.com", "staticorigin.wixstatic.com", "music.wixstatic.com"]
    is_asset_host = any(h in host for h in asset_hosts)
    asset_exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".avif", ".css", ".js", ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".mp4", ".webm", ".mp3", ".json", ".xml", ".map")
    if not (is_asset_host or ext in asset_exts):
        return url
    local = asset_local_name(url)
    if url not in url_map:
        data = fetch(url)
        if data is None and "enc_avif" in url:
            # Fallback: try without enc_avif/quality_auto (get original format)
            fallback_url = re.sub(r',enc_avif,quality_auto', '', url)
            if fallback_url != url:
                data = fetch(fallback_url)
                if data is not None:
                    local = asset_local_name(fallback_url)
        if data is not None:
            dest = ASSETS / local
            dest.write_bytes(data)
            url_map[url] = local
            print("Downloaded asset", local, len(data))
        else:
            url_map[url] = None
    mapped = url_map.get(url)
    if mapped is None:
        return url
    # compute relative path from file_path to assets/mapped
    rel = os.path.relpath(ASSETS / mapped, file_path.parent).replace("\\", "/")
    return rel

def process_file(file_path):
    text = file_path.read_bytes()
    try:
        content = text.decode("utf-8", errors="surrogateescape")
    except Exception:
        return
    changed = False
    # Find all absolute URLs in text (simple regex)
    urls = set(re.findall(r'https?://[^\s\'"\)<>{}]+', content))
    for url in sorted(urls, key=len, reverse=True):
        new_url = rewrite_url(url, file_path)
        if new_url != url:
            content = content.replace(url, new_url)
            changed = True
    # Also rewrite escaped URLs inside JSON (https:\/\/...)
    for m in re.finditer(r'https?:\\/\\/[^\s\'"\)<>{}]+', content):
        esc_url = m.group(0)
        plain_url = esc_url.replace('\\/', '/')
        new_url = rewrite_url(plain_url, file_path)
        if new_url != plain_url:
            esc_new = new_url.replace('/', '\\/')
            content = content.replace(esc_url, esc_new)
            changed = True
    if changed:
        file_path.write_bytes(content.encode("utf-8", errors="surrogateescape"))
        print("Rewrote", file_path)

# Process HTML files first, then CSS/JS
for ext in (".html", ".css", ".js", ".xml", ".json"):
    for f in ROOT.rglob(f"*{ext}"):
        process_file(f)

# Save mapping
map_file.write_text(json.dumps(url_map, indent=2, ensure_ascii=False), encoding="utf-8")
print("Done. Assets:", len([v for v in url_map.values() if v]))
if errors:
    print("Errors:", len(errors))
    for e in errors[:20]:
        print(e)
