"""Usecure weekly health check.

Re-verifies the numbers against HubSpot and writes them back into the vault, runs
integrity checks on the builds, lints the vault's own conventions, writes a dated
Check note, and posts a summary to Slack.

Exit 0 = clean, 1 = findings, 2 = could not run.
"""
import os, sys, json, re, datetime, urllib.request, subprocess

TOKEN   = os.environ.get("USECURE_HUBSPOT_TOKEN")
WEBHOOK = os.environ.get("USECURE_SLACK_WEBHOOK")
HERE    = os.path.dirname(os.path.abspath(__file__))
VAULT   = os.environ.get("VAULT_PATH", os.path.dirname(HERE))
B       = "https://api.hubapi.com"
LAUNCH  = "2026-07-21T00:00:00Z"
H       = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# stages that mean the lead is finished, whatever the calculated open flag says.
# one legacy record has hs_lead_is_open_v2 stuck true while sitting in Closed.
CLOSED_STAGES = ["unqualified-stage-id", "qualified-stage-id"]

def api(path, body=None):
    req = urllib.request.Request(B + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers=H, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read())

def count(obj, groups):
    return api(f"/crm/v3/objects/{obj}/search",
               {"filterGroups": [{"filters": g} for g in groups], "limit": 1}).get("total")

SINCE  = {"propertyName": "hs_createdate", "operator": "GTE", "value": LAUNCH}
A      = {"propertyName": "hs_v2_date_entered_attempting_stage_id_745667965", "operator": "HAS_PROPERTY"}
C      = {"propertyName": "hs_v2_date_entered_connected_stage_id_2058487257", "operator": "HAS_PROPERTY"}
Q      = {"propertyName": "hs_v2_date_entered_qualified_stage_id_233247981", "operator": "HAS_PROPERTY"}
OPEN   = {"propertyName": "hs_lead_is_open_v2", "operator": "EQ", "value": "true"}
LIVE   = {"propertyName": "hs_pipeline_stage", "operator": "NOT_IN", "values": CLOSED_STAGES}

# ------------------------------------------------------------------ metrics
def metrics():
    m = {}
    m["Conversions"] = count("0-420", [[SINCE]])
    leads = count("0-136", [[SINCE]])
    m["Leads created and routed"] = leads
    worked = count("0-136", [[SINCE, A], [SINCE, C], [SINCE, Q]])
    m["Picked up and worked"] = worked
    m["Qualified"] = count("0-136", [[SINCE, {"propertyName": "hs_pipeline_stage",
                                              "operator": "EQ", "value": "qualified-stage-id"}]])
    m["Open leads"] = count("0-136", [[OPEN, LIVE]])

    # net new event contacts, summed from the rollup on each event record
    total, after = 0, None
    while True:
        body = {"filterGroups": [{"filters": [{"propertyName": "hs_createdate",
                                               "operator": "GTE", "value": "2020-01-01T00:00:00Z"}]}],
                "properties": ["net_new_contacts"], "limit": 100}
        if after: body["after"] = after
        r = api("/crm/v3/objects/0-162/search", body)
        for e in r.get("results", []):
            v = e["properties"].get("net_new_contacts")
            if v: total += int(float(v))
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break
    m["Net new event contacts"] = total
    m["_worked_pct"] = round(worked / leads * 100) if leads else 0
    return m

# ---------------------------------------------------------------- integrity
DETAIL = []
OUT_OF_SYNC = []
REG_STATES = ("REGISTERED", "ATTENDED", "NO_SHOW")
LBL_REG, LBL_ATT = 14, 16

def breakdown(mid):
    recs, after = [], None
    while True:
        u = f"/marketing/v3/marketing-events/participations/{mid}/breakdown?limit=100"
        if after: u += f"&after={after}"
        r = api(u)
        recs += r.get("results", [])
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break
    return recs

def integrity():
    out = []

    for path in walk("Clients/Usecure/HubSpot"):
        f = frontmatter(path)
        wid, want = f.get("hubspot_id"), f.get("enabled")
        if not wid or want not in ("true", "false"): continue
        try:
            live = api(f"/automation/v4/flows/{wid}").get("isEnabled")
        except Exception:
            out.append(("workflow", f"{wid} could not be read from HubSpot")); continue
        if str(live).lower() != want:
            out.append(("drift", f"{os.path.basename(path)[:-3]} is "
                                 f"{'ON' if live else 'OFF'} in HubSpot, vault says {want}"))

    n = count("0-136", [[OPEN, LIVE, {"propertyName": "hubspot_owner_id",
                                      "operator": "NOT_HAS_PROPERTY"}]])
    if n: out.append(("unowned", f"{n} open lead(s) with no owner"))

    # Leaver ownership. The historic backlog (many thousands of companies against ~84
    # former users) is known and is not weekly news, so it is summarised in one line.
    # What IS actionable each week: open leads sitting with a leaver, and leaver-owned
    # companies that have a live deal on them.
    active = {o["id"] for o in api("/crm/v3/owners?limit=200")["results"]}
    leavers = [o for o in api("/crm/v3/owners?limit=200&archived=true")["results"]
               if o["id"] not in active]
    backlog_total, backlog_people = 0, 0
    leaver_deals, leaver_detail = 0, []
    for o in leavers:
        oid = o["id"]
        nm = (o.get("firstName","") + " " + o.get("lastName","")).strip() or o.get("email")
        n = count("0-136", [[OPEN, LIVE, {"propertyName": "hubspot_owner_id",
                                          "operator": "EQ", "value": oid}]])
        if n:
            out.append(("leaver", f"{n} open lead(s) still owned by {nm}, deactivated"))
        d = count("deals", [[{"propertyName": "hubspot_owner_id", "operator": "EQ", "value": oid},
                             {"propertyName": "hs_is_closed", "operator": "EQ", "value": "false"}]])
        if d:
            leaver_deals += d; leaver_detail.append((nm, d))
        co = count("companies", [[{"propertyName": "hubspot_owner_id",
                                   "operator": "EQ", "value": oid}]])
        if co:
            backlog_total += co; backlog_people += 1
    if leaver_deals:
        who = ", ".join(f"{n} ({d})" for n, d in sorted(leaver_detail, key=lambda x: -x[1]))
        out.append(("leaver deals", f"{leaver_deals} open deal(s) held by "
                                    f"{len(leaver_detail)} deactivated users"))
        DETAIL.append(f"Open deals by deactivated owner: {who}")
    if backlog_total:
        out.append(("backlog", f"{backlog_total:,} companies owned by {backlog_people} "
                               f"deactivated users - known backlog, not new"))

    n = count("deals", [[{"propertyName": "createdate", "operator": "GTE", "value": LAUNCH},
                         {"propertyName": "pipeline", "operator": "EQ", "value": "default"},
                         {"propertyName": "num_associated_contacts", "operator": "EQ", "value": "0"}]])
    if n: out.append(("deals", f"{n} new-business deal(s) since launch with no contact"))

    for prop, obj in (("trigger_lead_reassignment", "companies"),
                      ("trigger_multithread_alert", "companies"),
                      ("trigger_unowned_lead_routing", "contacts")):
        try:
            n = count(obj, [[{"propertyName": prop, "operator": "HAS_PROPERTY"}]])
        except Exception: continue
        if n: out.append(("stuck trigger", f"{n} {obj[:-1]} record(s) with {prop} still set - "
                                           f"the second workflow did not run"))


    # Events: does every marketing event that has real people on it have a custom event
    # object, and do the registrant/attendee counts agree? A shortfall on the custom object
    # means association workflows missed people, which silently drops them out of net new
    # tagging and deal attribution.
    me, after = [], None
    while True:
        u = "/marketing/v3/marketing-events/?limit=100" + (f"&after={after}" if after else "")
        try: r = api(u)
        except Exception: break
        me += r.get("results", [])
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break
    ev, after = [], None
    while True:
        body = {"filterGroups": [{"filters": [{"propertyName": "hs_createdate",
                                               "operator": "GTE", "value": "2020-01-01T00:00:00Z"}]}],
                "properties": ["hs_name", "marketing_event_id",
                               "total_registrations", "total_attendees"], "limit": 100}
        if after: body["after"] = after
        r = api("/crm/v3/objects/0-162/search", body)
        ev += r.get("results", [])
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break

    linked = {e["properties"].get("marketing_event_id"): e for e in ev
              if e["properties"].get("marketing_event_id")}
    orphaned = [m for m in me
                if str(m.get("objectId")) not in linked
                and ((m.get("registrants") or 0) > 0 or (m.get("attendees") or 0) > 0)]
    if orphaned:
        out.append(("events", f"{len(orphaned)} marketing event(s) with registrants but no "
                              f"event record - invisible to attribution"))
        for m in orphaned[:10]:
            DETAIL.append(f"No event record: {m.get('eventName','')[:60]} "
                          f"({m.get('registrants')} reg, {m.get('attendees')} att)")

    # Compare against the participation records, NOT the marketing event's registrants
    # and attendees fields. Those are counters the integration maintains and they sit
    # 1-2 high - they double-count re-registrations and keep counts for merged records.
    # Comparing against them reported a permanent phantom gap.
    short_r = short_a = short_n = 0
    for mid, e in linked.items():
        p = e["properties"]
        tr = int(float(p.get("total_registrations") or 0))
        ta = int(float(p.get("total_attendees") or 0))
        try:
            recs = breakdown(mid)
        except Exception:
            continue
        want_r, want_a = set(), set()
        for r in recs:
            cid = str(r.get("associations", {}).get("contact", {}).get("contactId") or "")
            st = r.get("properties", {}).get("attendanceState")
            if not cid or st not in REG_STATES: continue   # CANCELLED excluded on purpose
            want_r.add(cid)
            if st == "ATTENDED": want_a.add(cid)
        dr, da = len(want_r) - tr, len(want_a) - ta
        if dr > 0 or da > 0:
            short_n += 1; short_r += max(dr, 0); short_a += max(da, 0)
            OUT_OF_SYNC.append((e["id"], mid, p.get("hs_name", "")))
            DETAIL.append(f"Short on {p.get('hs_name','')[:52]}: "
                          f"{tr}/{len(want_r)} registered, {ta}/{len(want_a)} attended")

    if short_n:
        out.append(("events", f"{short_n} event(s) out of sync with their marketing event - "
                              f"{short_r} registrant(s) and {short_a} attendee(s) missing"))

    unl = 0
    after = None
    while True:
        body = {"filterGroups": [{"filters": [{"propertyName": "hs_createdate",
                                               "operator": "GTE", "value": "2020-01-01T00:00:00Z"}]}],
                "properties": ["hs_name"], "limit": 100}
        if after: body["after"] = after
        r = api("/crm/v3/objects/0-162/search", body)
        for e in r.get("results", []):
            try:
                d = api(f"/crm/v4/objects/0-162/{e['id']}/associations/deals?limit=500")
            except Exception: continue
            for x in d.get("results", []):
                if not [t.get("label") for t in x["associationTypes"] if t.get("label")]: unl += 1
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break
    if unl: out.append(("events", f"{unl} event-deal link(s) with no Sourced/Influenced label"))
    return out

# ---------------------------------------------------------------- vault io
def walk(rel):
    for root, _, files in os.walk(os.path.join(VAULT, rel)):
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
        return old if old != str(value) else None
    return "MISSING"

def run_lint():
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, "lint.py")],
                           capture_output=True, text=True, timeout=120,
                           env={**os.environ, "VAULT_PATH": VAULT})
        return p.returncode, p.stdout.strip()
    except Exception as e:
        return 2, f"lint could not run: {e}"

def write_check(today, m, findings, moved, lint_rc, lint_out):
    d = os.path.join(VAULT, "Clients/Usecure/Checks")
    os.makedirs(d, exist_ok=True)
    L = ["---", "type: check", "client: Usecure", f"date: {today}",
         f"outcome: {'clean' if not findings and lint_rc == 0 else 'findings'}",
         "automated: true", "---", f"# Automated health check, {today}", "",
         "Run by `scripts/checks.py`. The metric notes below have been updated in place.",
         "", "## Numbers", "", "| Metric | Now | Was |", "|---|---|---|"]
    for k, v in m.items():
        if k.startswith("_"): continue
        was = moved.get(k)
        L.append(f"| [[{k}]] | {v} | {was if was and was != 'MISSING' else '-'} |")
    L += ["", f"Worked rate **{m['_worked_pct']}%** of leads since launch. Read that alongside",
          "[[Picked up and worked]] - most qualified leads self-convert without a rep touch.", ""]
    L += ["## Build integrity", ""]
    L += [f"- **{c}** - {msg}" for c, msg in findings] or ["Every check passed."]
    if DETAIL:
        L += ["", "## Detail", ""] + [f"- {d}" for d in DETAIL]
    L += ["", "## Vault lint", "", "```", lint_out or "clean", "```"]
    open(os.path.join(d, f"{today} Automated health check.md"), "w").write("\n".join(L) + "\n")

def slack(text):
    if not WEBHOOK:
        print("(no webhook set, skipping Slack)"); return
    try:
        urllib.request.urlopen(urllib.request.Request(
            WEBHOOK, data=json.dumps({"text": text}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
        print("posted to Slack")
    except Exception as e:
        print("slack post failed:", e, file=sys.stderr)


# ------------------------------------------------------------------- repair
def current_labels(event_id):
    """contactId -> set of typeIds currently on the pair."""
    cur, after = {}, None
    while True:
        u = f"/crm/v4/objects/0-162/{event_id}/associations/contacts?limit=500"
        if after: u += f"&after={after}"
        r = api(u)
        for x in r.get("results", []):
            cur.setdefault(str(x["toObjectId"]), set()).update(
                t["typeId"] for t in x["associationTypes"] if t.get("label"))
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break
    return cur

def repair_event(event_id, mid):
    """Add missing Registered/Attended labels. Returns (added_reg, added_att, failed).

    A v4 association PUT REPLACES the whole label set for a pair, so the desired set
    must include everything that is already there - including the Net new label, or
    it gets stripped. Learned the hard way.
    """
    recs = breakdown(mid)
    want = {}
    for r in recs:
        cid = str(r.get("associations", {}).get("contact", {}).get("contactId") or "")
        st = r.get("properties", {}).get("attendanceState")
        if not cid or st not in REG_STATES: continue
        want.setdefault(cid, set()).add(LBL_REG)
        if st == "ATTENDED": want[cid].add(LBL_ATT)
    cur = current_labels(event_id)
    added_r = added_a = 0
    failed = []
    for cid, need in want.items():
        have = cur.get(cid, set())
        if need <= have: continue
        merged = have | need                      # never drop an existing label
        body = [{"associationCategory": "USER_DEFINED", "associationTypeId": t} for t in sorted(merged)]
        try:
            req = urllib.request.Request(
                f"{B}/crm/v4/objects/0-162/{event_id}/associations/0-1/{cid}",
                data=json.dumps(body).encode(), headers=H, method="PUT")
            urllib.request.urlopen(req, timeout=30).read()
            if LBL_REG in need - have: added_r += 1
            if LBL_ATT in need - have: added_a += 1
        except Exception as e:
            failed.append(f"{cid}: {e}")
    if (added_r or added_a):
        try:  # nudge net new tagging and deal attribution to recompute
            api(f"/crm/v3/objects/0-162/{event_id}")
            req = urllib.request.Request(
                f"{B}/crm/v3/objects/0-162/{event_id}",
                data=json.dumps({"properties": {"run_deal_attribution": "true"}}).encode(),
                headers=H, method="PATCH")
            urllib.request.urlopen(req, timeout=30).read()
        except Exception:
            pass
    return added_r, added_a, failed

# ---------------------------------------------------------------- main
def main():
    global DETAIL
    if not TOKEN:
        print("USECURE_HUBSPOT_TOKEN is not set", file=sys.stderr); return 2
    today = datetime.date.today().isoformat()
    try:
        m = metrics()
    except Exception as e:
        slack(f":rotating_light: *Usecure health check - {today}*\n"
              f"Could not read HubSpot: `{e}`. The result is unknown, not clear.")
        print("could not read HubSpot:", e, file=sys.stderr); return 2

    moved = {}
    for k, v in m.items():
        if k.startswith("_"): continue
        old = update_metric(k, v, today)
        if old: moved[k] = old
    missing = [k for k, v in moved.items() if v == "MISSING"]

    findings = integrity()

    repaired = None
    if "--fix" in sys.argv and OUT_OF_SYNC:
        tr = ta = 0; tf = []
        for eid, mid, nm in OUT_OF_SYNC:
            r, a, f = repair_event(eid, mid)
            tr += r; ta += a; tf += f
            if r or a: DETAIL.append(f"Repaired {nm[:52]}: +{r} registered, +{a} attended")
        if tr or ta:
            repaired = f"repaired {tr} registrant and {ta} attendee association(s) "\
                       f"across {len(OUT_OF_SYNC)} event(s)"
            findings = [f for f in findings if f[0] != "events" or "out of sync" not in f[1]]
            findings.append(("repaired", repaired))
        if tf:
            findings.append(("repair failed", f"{len(tf)} association(s) could not be created"))
            DETAIL += tf[:10]

    lint_rc, lint_out = run_lint()
    write_check(today, m, findings, moved, lint_rc, lint_out)

    clean = not findings and lint_rc == 0 and not missing
    head = ":white_check_mark:" if clean else ":warning:"
    txt = (f"{head} *Usecure - weekly health check*\n"
           f"*{m['Leads created and routed']}* leads · *{m['Picked up and worked']}* worked "
           f"({m['_worked_pct']}%) · *{m['Qualified']}* qualified · *{m['Open leads']}* open · "
           f"*{m['Net new event contacts']}* net new from events\n")
    if clean:
        txt += "All checks passed. Metric notes refreshed in the vault."
    else:
        for c, msg in findings: txt += f"• {c}: {msg}\n"
        for k in missing: txt += f"• vault: no metric note for {k}\n"
        if lint_rc == 1:
            first = lint_out.split("\n")[0] if lint_out else "problems found"
            txt += f"• vault lint: {first}\n"
    slack(txt.rstrip())
    print(txt)
    for k, v in m.items():
        if not k.startswith("_"):
            print(f"  {k}: {v}" + (f"  (was {moved[k]})" if moved.get(k) not in (None,"MISSING") else ""))
    print(f"\n{lint_out}")
    return 0 if clean else 1

if __name__ == "__main__":
    sys.exit(main())