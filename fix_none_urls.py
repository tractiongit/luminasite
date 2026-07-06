#!/usr/bin/env python3
"""Remove None entries from urlmap.json so localize.py will retry downloading them."""
import json
from pathlib import Path

map_file = Path(__file__).parent / "clone" / "assets" / "urlmap.json"
m = json.loads(map_file.read_text(encoding="utf-8"))

before = len(m)
m = {k: v for k, v in m.items() if v is not None}
after = len(m)

map_file.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Removed {before - after} None entries. Remaining: {after}")
