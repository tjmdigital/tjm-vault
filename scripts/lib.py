"""Shared plumbing for client health checks.

Everything that is not about a specific client lives here: the HubSpot API, writing
values back into vault metric notes, composing the Check note, running the lint, and
posting to Slack. A client module supplies only what to count and what to check.
"""
import os, sys, json, re, datetime, urllib.request, subprocess

HERE  = os.path.dirname(os.path.abspath(__file__))
VAULT = os.environ.get("VAULT_PATH", os.path.dirname(HERE))
B     = "https://api.hubapi.com"


class Client:
    """One client's HubSpot connection and vault folder."""

    def __init__(self, name, token_env, portal=None, launch=None):
        self.name    = name
        self.portal  = portal
        self.launch  = launch
        self.token   = os.environ.get(token_env)
        self.token_env = token_env
        self.folder  = os.path.join(VAULT, "Clients", name)
        self.detail  = []
        self.H = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    # ---------------------------------------------------------- hubspot
    def api(self, path, body=None, method=None):
        req = urllib.request.Request(
            B + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers=self.H,
            method=method or ("POST" if body is not None else "GET"))
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}

    def count(self, obj, groups):
        return self.api(f"/crm/v3/objects/{obj}/search",
                        {"filterGroups": [{"filters": g} for g in groups],
                         "limit": 1}).get("total")

    def page(self, obj, props, filters=None):
        """Every record of an object type, paged."""
        out, after = [], None
        f = filters or [{"propertyName": "hs_createdate", "operator": "GTE",
                         "value": "2020-01-01T00:00:00Z"}]
        while True:
            body = {"filterGroups": [{"filters": f}], "properties": props, "limit": 100}
            if after: body["after"] = after
            r = self.api(f"/crm/v3/objects/{obj}/search", body)
            out += r.get("results", [])
            after = r.get("paging", {}).get("next", {}).get("after")
            if not after: return out

    def owners(self):
        """(active ids, list of deactivated owner records)"""
        active = {o["id"] for o in self.api("/crm/v3/owners?limit=200")["results"]}
        gone = [o for o in self.api("/crm/v3/owners?limit=200&archived=true")["results"]
                if o["id"] not in active]
        return active, gone

    # ------------------------------------------------------------ vault
    def notes(self, sub):
        d = os.path.join(self.folder, sub)
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(".md"): yield os.path.join(root, f)

    def frontmatter(self, path):
        s = open(path).read()
        if not s.startswith("---"): return {}
        return {k.strip(): v.strip() for k, v in
                (l.split(":", 1) for l in s.split("---")[1].split("\n")
                 if ":" in l and not l.startswith(" "))}

    def update_metric(self, name, value, today):
        """Write a value back to its metric note. Returns the old value if it changed,
        'MISSING' if there is no note for it, or None."""
        for path in self.notes("Metrics"):
            if os.path.basename(path)[:-3].lower() != name.lower(): continue
            s = open(path).read()
            if "status: retired" in s: return None
            old = re.search(r"^value: (.*)$", s, re.M)
            old = old.group(1).strip() if old else None
            s = re.sub(r"^value: .*$", f"value: {value}", s, count=1, flags=re.M)
            s = re.sub(r"^verified: .*$", f"verified: {today}", s, count=1, flags=re.M)
            open(path, "w").write(s)
            return old if old != str(value) else None
        return "MISSING"

    def note(self, msg):
        """Detail for the Check note but not for Slack."""
        self.detail.append(msg)


# ------------------------------------------------------------------ shared
def run_lint():
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, "lint.py")],
                           capture_output=True, text=True, timeout=180,
                           env={**os.environ, "VAULT_PATH": VAULT})
        return p.returncode, p.stdout.strip()
    except Exception as e:
        return 2, f"lint could not run: {e}"


def write_check(c, today, metrics, moved, findings, lint_out):
    d = os.path.join(c.folder, "Checks")
    os.makedirs(d, exist_ok=True)
    L = ["---", "type: check", f"client: {c.name}", f"date: {today}",
         f"outcome: {'clean' if not findings else 'findings'}",
         "automated: true", "---", f"# Automated health check, {today}", "",
         "Run by `scripts/run.py`. The metric notes below were updated in place.",
         "", "## Numbers", "", "| Metric | Now | Was |", "|---|---|---|"]
    for k, v in metrics.items():
        if k.startswith("_"): continue
        was = moved.get(k)
        L.append(f"| [[{k}]] | {v} | {was if was and was != 'MISSING' else '-'} |")
    L += ["", "## Findings", ""]
    L += [f"- **{cat}** - {msg}" for cat, msg in findings] or ["Every check passed."]
    if c.detail:
        L += ["", "## Detail", ""] + [f"- {x}" for x in c.detail]
    L += ["", "## Vault lint", "", "```", lint_out or "clean", "```"]
    open(os.path.join(d, f"{today} Automated health check.md"), "w").write("\n".join(L) + "\n")


def slack(text, webhook_env="TJM_SLACK_WEBHOOK"):
    hook = os.environ.get(webhook_env) or os.environ.get("USECURE_SLACK_WEBHOOK")
    if not hook:
        print("(no webhook set, skipping Slack)"); return
    try:
        urllib.request.urlopen(urllib.request.Request(
            hook, data=json.dumps({"text": text}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
        print("posted to Slack")
    except Exception as e:
        print("slack post failed:", e, file=sys.stderr)
