#!/usr/bin/env python3
"""Build dist/nlsql-openai-plugin.zip for upload at platform.openai.com/plugins.

The upload wants the portable Agent Plugins layout: plugin.json and mcp.json at
the zip root, plus skills/ and assets/. The repo root can't hold that layout
because its mcp.json is Cursor's format, so the package is generated from
.codex-plugin/plugin.json. That keeps one source for the Codex install and the
upload.

Run from anywhere:  python3 scripts/build-openai-package.py
"""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "nlsql-openai-plugin.zip"
IDENTITY = ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")
FIXED_TIME = (2026, 1, 1, 0, 0, 0)  # stable timestamps, so an unchanged build gives an identical zip

codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())

plugin = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"}
plugin.update({k: codex[k] for k in IDENTITY if k in codex})
plugin["extensions"] = {"com.openai": {"interface": codex["interface"]}}

mcp = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
    "mcpServers": codex["mcpServers"],
}


def files_under(rel):
    return sorted(p for p in (ROOT / rel).rglob("*") if p.is_file() and p.name != ".DS_Store")


def add(zf, arcname, data):
    info = zipfile.ZipInfo(arcname, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT, "w") as zf:
    add(zf, "plugin.json", json.dumps(plugin, indent=2) + "\n")
    add(zf, "mcp.json", json.dumps(mcp, indent=2) + "\n")
    for p in files_under("skills") + files_under("assets"):
        add(zf, p.relative_to(ROOT).as_posix(), p.read_bytes())

print(f"wrote {OUT.relative_to(ROOT)}")
with zipfile.ZipFile(OUT) as zf:
    for n in zf.namelist():
        print("  ", n)
