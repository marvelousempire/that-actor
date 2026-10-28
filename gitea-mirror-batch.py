#!/usr/bin/env python3
"""
Gitea Mirror Batch — registers push mirrors for the fifteen core repos.
Each repo on GitHub gets a push mirror to the private Gitea instance.
Run from a machine with Gitea admin access. Requires GITEA_URL and GITEA_TOKEN.
"""
import json, os, sys, urllib.request

GITEA_URL = os.environ.get("GITEA_URL", "").rstrip("/")
GITEA_TOKEN = os.environ.get("GITEA_TOKEN", "")
OWNER = "marvelousempire"

CORE_REPOS = [
    "actorTHAT", "CCK-that", "sense-that-studio", "camera-that", "moment-that",
    "euclidean-canon-canvas", "philosophy-chromatophore", "stack-that", "gameThat",
    "RomThat", "contract-that", "skillTHAT", "define-that", "Automata", "ReadyPlay",
]

def api(method, path, body=None):
    req = urllib.request.Request(
        f"{GITEA_URL}{path}",
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"token {GITEA_TOKEN}", "Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def main():
    if not GITEA_URL or not GITEA_TOKEN:
        print("Set GITEA_URL and GITEA_TOKEN environment variables.")
        sys.exit(1)
    for repo in CORE_REPOS:
        path = f"/api/v1/repos/{OWNER}/{repo}/push_mirrors"
        body = {
            "remote_address": f"https://github.com/{OWNER}/{repo}.git",
            "remote_username": OWNER,
            "remote_password": os.environ.get("GH_TOKEN", ""),
            "interval": "8h",
            "sync_on_commit": True,
        }
        status, result = api("POST", path, body)
        print(f"{repo}: {status} — {result if isinstance(result, str) else 'ok'}")

if __name__ == "__main__":
    main()
