#!/usr/bin/env python3
"""Report which image backends can run here. Never prints key values.

Usage: python3 check_setup.py [--json]
Exit 0 when at least one backend is usable, else 2.
"""

from __future__ import annotations

import argparse
import json
import shutil
import socket
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from api_backends import google_key, xai_key  # noqa: E402

HOSTS = {"gemini-api": "generativelanguage.googleapis.com", "xai-api": "api.x.ai"}


def reachable(host: str) -> bool:
    """True when an HTTPS request to host gets any HTTP answer (even 4xx)."""
    try:
        urllib.request.urlopen(f"https://{host}/", timeout=8)
        return True
    except urllib.error.HTTPError:
        return True
    except (urllib.error.URLError, socket.timeout, OSError):
        return False


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-network", action="store_true", help="Skip reachability probes")
    args = p.parse_args()

    report: dict[str, dict] = {}
    for cli in ("imagen", "grok-img", "codex"):
        path = shutil.which(cli)
        report[cli] = {"kind": "cli", "installed": bool(path), "path": path}
    for name, finder in (("gemini-api", google_key), ("xai-api", xai_key)):
        key, where = finder()
        entry = {"kind": "rest", "key": where or "missing", "host": HOSTS[name]}
        if key and not args.no_network:
            entry["reachable"] = reachable(HOSTS[name])
        report[name] = entry

    usable = [
        n
        for n, e in report.items()
        if (e["kind"] == "cli" and e["installed"])
        or (e["kind"] == "rest" and e["key"] != "missing" and e.get("reachable", True))
    ]

    if args.json:
        print(json.dumps({"usable": usable, "backends": report}, indent=2))
    else:
        for name, e in report.items():
            if e["kind"] == "cli":
                state = f"installed at {e['path']}" if e["installed"] else "not installed"
            else:
                state = f"key {e['key']}"
                if "reachable" in e:
                    state += ", host reachable" if e["reachable"] else ", HOST BLOCKED"
            print(f"{name:11} {state}")
        print()
        print("usable:", ", ".join(usable) if usable else "none")
        if not usable:
            print(
                "\nTo enable generation, do one of:\n"
                "  - Put GEMINI_API_KEY=... (and/or XAI_API_KEY=...) in\n"
                "    ~/.config/spillwave/image-keys.env, or export it in the shell.\n"
                "  - Install a CLI: pip install -U gemini-imagen  (imagen),\n"
                "    npm install -g grok-image-cli  (grok-img), or codex.\n"
                "  - In a claude.ai cloud session, API hosts are blocked unless an\n"
                "    org admin allows them; run from Claude Desktop/Cowork instead."
            )
    return 0 if usable else 2


if __name__ == "__main__":
    sys.exit(main())
