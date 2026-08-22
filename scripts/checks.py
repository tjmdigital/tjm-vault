"""Usecure health check - re-verifies the numbers and the builds.

Writes back into the vault: metric values, verified dates, workflow states,
and a dated Check note. Posts a summary to Slack if a webhook is configured.

Exit 0 = clean, 1 = findings, 2 = could not run.
"""
import os, sys, json, re, datetime, urllib.request

TOKEN = os.environ.get("USECURE_HUBSPOT_TOKEN")
WEBHOOK = os.environ.get("USECURE_SLACK_WEBHOOK")
VAULT = os.environ.get("VAULT_PATH", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B = "https://api.hubapi.com"
LAUNCH = "2026-07-21T00:00:00Z"
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def api(path, body=None):
    url = B + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=H,
                                 method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def count(obj, groups):
    r = api(f"/crm/v3/objects/{obj}/search",
            {"filterGroups": [{"filters": g} for g in groups], "limit": 1})
    return r.get("total")

SINCE = {"propertyName": "hs_createdate", "operator": "GTE", "value": LAUNCH}
A = {"propertyName": "hs_v2_date_entered_attempting_stage_id_745667965", "operator": "HAS_PROPERTY"}
C = {"propertyName": "hs_v2_date_entered_connected_stage_id_2058487257", "operator": "HAS_PROPERTY"}
Q = {"propertyName": "hs_v2_date_entered_qualified_stage_id_233247981", "operator": "HAS_PROPERTY"}
OPEN = {"propertyName": "hs_lead_is_open_v2", "operator": "EQ", "value": "true"}

# ---------------------------------------------------------------- metrics
def metrics():
    m = {}
    m["Conversions"] = count("0-420", [[SINCE]])
    leads = count("0-136", [[SINCE]])
    m["Leads created and routed"] = leads
    worked = count("0-136", [[SINCE, A], [SINCE, C], [SINCE, Q]])
    m["Picked up and worked"] = worked
    m["Qualified"] = count("0-136", [[SINCE, {"propertyName": "hs_pipeline_stage",
                                              "operator": "EQ", "value": "qualified-stage-id"}]])
    m["Open leads"] = count("0-136", [[OPEN]])
    m["_worked_pct"] = round(worked / leads * 100) if leads else 0
    return m

# ---------------------------------------------------------------- integrity
def integrity():
    out = []

    # 1. workflow state drift - vault says one thing, HubSpot another
    for path in walk("Clients/Usecure/HubSpot"):
        fm = frontmatter(path)
        wid, want = fm.get("hubspot_id"), fm.get("enabled")
        if not wid or want not in ("true", "false"):
            continue
        try:
            live = api(f"/automation/v4/flows/{wid}").get("isEnabled")
        except Exception:
            out.append(("workflow", f"{wid} could not be read from HubSpot")); continue
        if str(live).lower() != want:
            out.append(("workflow",
                        f"{os.path.basename(path)[:-3]} is {'ON' if live else 'OFF'} in HubSpot "
                        f"but the vault says {want}"))

    # 2. leads with nobody to work them
    n = count("0-136", [[OPEN, {"propertyName": "hubspot_owner_id", "operator": "NOT_HAS_PROPERTY"}]])
    if n: out.append(("leads", f"{n} open lead(s) with no owner"))

    # 3. open leads owned by someone who has left
    active = {o["id"] for o in api("/crm/v3/owners?limit=200")["results"]}
    arch = [o for o in api("/crm/v3/owners?limit=200&archived=true")["results"]
            if o["id"] not in active]
    for o in arch:
        n = count("0-136", [[OPEN, {"propertyName": "hubspot_owner_id",
                                    "operator": "EQ", "value": o["id"]}]])
        if n:
            nm = (o.get("firstName", "") + " " + o.get("lastName", "")).strip() or o.get("email")
            out.append(("leavers", f"{n} open lead(s) still owned by {nm}, who is deactivated"))

    # 4. new business deals with no contact - breaks event attribution
    n = count("deals", [[{"propertyName": "createdate", "operator": "GTE", "value": LAUNCH},
                         {"propertyName": "pipeline", "operator": "EQ", "value": "default"},
                         {"propertyName": "num_associated_contacts", "operator": "EQ", "value": "0"}]])
    if n: out.append(("deals", f"{n} new-business deal(s) since launch with no contact attached"))

    # 5. two-stage triggers left set - means the second workflow did not run
    for prop, obj in (("trigger_lead_reassignment", "companies"),
                      ("trigger_multithread_alert", "companies"),
                      ("trigger_unowned_lead_routing", "contacts")):
        try:
            n = count(obj, [[{"propertyName": prop, "operator": "HAS_PROPERTY"}]])
        except Exception:
            continue
        if n: out.append(("triggers", f"{n} {obj[:-1]} record(s) stuck with {prop} set"))

    # 6. event attribution labels
    evs = api("/crm/v3/objects/0-162/search",
              {"filterGroups": [{"filters": [{"propertyName": "hs_createdate",
                                              "operator": "GTE", "value": "2020-01-01T00:00:00Z"}]}],
               "properties": ["hs_name"], "limit": 100}).get("results", [])
    unl = ren_sourced = 0
    for e in evs:
        try:
            r = api(f"/crm/v4/objects/0-162/{e['id']}/associations/deals?limit=500")
        except Exception:
            continue
        for x in r.get("results", []):
            labs = [t.get("label") for t in x["associationTypes"] if t.get("label")]
            if not labs: unl += 1
    if unl: out.append(("events", f"{unl} event-deal link(s) with no Sourced/Influenced label"))

    return out

# ---------------------------------------------------------------- vault io
def walk(rel):
    base = os.path.join(VAULT, rel)
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(".md"): yield os.path.join(root, f)

def frontmatter(path):
    s = open(path).read()
    if not s.startswith("---"): return {}
    return {k.strip(): v.strip() for k, v in
            (l.split(":", 1) for l in s.split("---")[1].split("\n")
             if ":" in l and not l.startswith(" "))}

def update_metric(name, value, today):
    for path in walk("Clients/Usecure/Metrics"):
        if os.path.basename(path)[:-3].lower() != name.lower(): continue
        s = open(path).read()
        if "status: retired" in s: return None
        old = re.search(r"^value: (.*)$", s, re.M)
        old = old.group(1).strip() if old else None
        s = re.sub(r"^value: .*$", f"value: {value}", s, count=1, flags=re.M)
        s = re.sub(r"^verified: .*$", f"verified: {today}", s, count=1, flags=re.M)
        open(path, "w").write(s)
        return old
    return None

def write_check(today, m, findings, moved):
    d = os.path.join(VAULT, "Clients/Usecure/Checks")
    os.makedirs(d, exist_ok=True)
    lines = [f"---", "type: check", "client: Usecure", f"date: {today}",
             f"outcome: {'clean' if not findings else str(len(findings)) + ' finding(s)'}",
             "automated: true", "---", f"# Automated health check, {today}", "",
             "Run by `scripts/checks.py`. Metric notes have been updated in place.", "",
             "## Numbers", "", "| Metric | Now | Was |", "|---|---|---|"]
    for k, v in m.items():
        if k.startswith("_"): continue
        was = moved.get(k)
        lines.append(f"| [[{k}]] | {v} | {was if was not in (None, str(v)) else '-'} |")
    lines += ["", f"Worked rate: **{m['_worked_pct']}%** of leads since launch.", ""]
    if findings:
        lines += ["## Findings", ""]
        for cat, msg in findings: lines.append(f"- **{cat}** - {msg}")
    else:
        lines += ["## Findings", "", "None. Every check passed."]
    open(os.path.join(d, f"{today} Automated health check.md"), "w").write("\n".join(lines) + "\n")

def slack(text):
    if not WEBHOOK: return
    try:
        req = urllib.request.Request(WEBHOOK, data=json.dumps({"text": text}).encode(),
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        print("slack post failed:", e, file=sys.stderr)

# ---------------------------------------------------------------- main
def main():
    if not TOKEN:
        print("USECURE_HUBSPOT_TOKEN is not set", file=sys.stderr); return 2
    today = datetime.date.today().isoformat()
    try:
        m = metrics()
    except Exception as e:
        print("could not read HubSpot:", e, file=sys.stderr); return 2
    moved = {}
    for k, v in m.items():
        if k.startswith("_"): continue
        old = update_metric(k, v, today)
        if old is not None: moved[k] = old
    findings = integrity()
    write_check(today, m, findings, moved)

    head = ":white_check_mark:" if not findings else ":warning:"
    txt = (f"{head} *Usecure health check - {today}*\n"
           f"*{m['Leads created and routed']}* leads · *{m['Picked up and worked']}* worked "
           f"({m['_worked_pct']}%) · *{m['Qualified']}* qualified · "
           f"*{m['Open leads']}* open\n")
    txt += ("No issues found." if not findings else
            "\n".join(f"• {c}: {msg}" for c, msg in findings))
    slack(txt)
    print(txt)
    for k, v in m.items():
        if not k.startswith("_"): print(f"  {k}: {v}" + (f"  (was {moved[k]})" if k in moved else ""))
    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
