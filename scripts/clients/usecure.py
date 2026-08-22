"""Usecure - what to count and what to check. Portal 2707865.

Everything generic lives in lib.py. This file should only ever contain things that
are true of Usecure specifically.
"""
NAME      = "Usecure"
TOKEN_ENV = "USECURE_HUBSPOT_TOKEN"
PORTAL    = 2707865
LAUNCH    = "2026-07-21T00:00:00Z"          # the new inbound process went live

SINCE  = {"propertyName": "hs_createdate", "operator": "GTE", "value": LAUNCH}
A      = {"propertyName": "hs_v2_date_entered_attempting_stage_id_745667965", "operator": "HAS_PROPERTY"}
C      = {"propertyName": "hs_v2_date_entered_connected_stage_id_2058487257", "operator": "HAS_PROPERTY"}
Q      = {"propertyName": "hs_v2_date_entered_qualified_stage_id_233247981", "operator": "HAS_PROPERTY"}
OPEN   = {"propertyName": "hs_lead_is_open_v2", "operator": "EQ", "value": "true"}
# one legacy lead has the calculated open flag stuck true while sitting in Closed
LIVE   = {"propertyName": "hs_pipeline_stage", "operator": "NOT_IN",
          "values": ["unqualified-stage-id", "qualified-stage-id"]}

REG_STATES = ("REGISTERED", "ATTENDED", "NO_SHOW")   # CANCELLED excluded on purpose
LBL_REG, LBL_ATT = 14, 16                            # both USER_DEFINED, not HubSpot


def metrics(c):
    m = {}
    m["Conversions"] = c.count("0-420", [[SINCE]])
    leads = c.count("0-136", [[SINCE]])
    m["Leads created and routed"] = leads
    worked = c.count("0-136", [[SINCE, A], [SINCE, C], [SINCE, Q]])
    m["Picked up and worked"] = worked
    m["Qualified"] = c.count("0-136", [[SINCE, {"propertyName": "hs_pipeline_stage",
                                                "operator": "EQ", "value": "qualified-stage-id"}]])
    m["Open leads"] = c.count("0-136", [[OPEN, LIVE]])
    m["Net new event contacts"] = sum(
        int(float(e["properties"].get("net_new_contacts") or 0))
        for e in c.page("0-162", ["net_new_contacts"]))
    m["_headline"] = (f"*{leads}* leads · *{worked}* worked "
                      f"({round(worked / leads * 100) if leads else 0}%) · "
                      f"*{m['Qualified']}* qualified · *{m['Open leads']}* open · "
                      f"*{m['Net new event contacts']}* net new from events")
    return m


def breakdown(c, mid):
    recs, after = [], None
    while True:
        u = f"/marketing/v3/marketing-events/participations/{mid}/breakdown?limit=100"
        if after: u += f"&after={after}"
        r = c.api(u)
        recs += r.get("results", [])
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: return recs


def wanted_labels(c, mid):
    """contactId -> set of label typeIds the participation data says it should have."""
    want = {}
    for r in breakdown(c, mid):
        cid = str(r.get("associations", {}).get("contact", {}).get("contactId") or "")
        st = r.get("properties", {}).get("attendanceState")
        if not cid or st not in REG_STATES: continue
        want.setdefault(cid, set()).add(LBL_REG)
        if st == "ATTENDED": want[cid].add(LBL_ATT)
    return want


def current_labels(c, event_id):
    cur, after = {}, None
    while True:
        u = f"/crm/v4/objects/0-162/{event_id}/associations/contacts?limit=500"
        if after: u += f"&after={after}"
        r = c.api(u)
        for x in r.get("results", []):
            cur.setdefault(str(x["toObjectId"]), set()).update(
                t["typeId"] for t in x["associationTypes"] if t.get("label"))
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: return cur


def checks(c):
    out, repairable = [], []

    # workflow state drift - the vault says one thing, HubSpot another
    for path in c.notes("HubSpot"):
        f = c.frontmatter(path)
        wid, want = f.get("hubspot_id"), f.get("enabled")
        if not wid or want not in ("true", "false"): continue
        try:
            live = c.api(f"/automation/v4/flows/{wid}").get("isEnabled")
        except Exception:
            out.append(("workflow", f"{wid} could not be read")); continue
        if str(live).lower() != want:
            out.append(("drift", f"{path.split('/')[-1][:-3]} is "
                                 f"{'ON' if live else 'OFF'} in HubSpot, vault says {want}"))

    n = c.count("0-136", [[OPEN, LIVE,
                           {"propertyName": "hubspot_owner_id", "operator": "NOT_HAS_PROPERTY"}]])
    if n: out.append(("unowned", f"{n} open lead(s) with no owner"))

    # leavers. The company backlog is known and old, so it gets one summary line;
    # open leads and open deals with a dead owner are the actionable part.
    _, gone = c.owners()
    deals = detail = 0
    who, backlog, people = [], 0, 0
    for o in gone:
        nm = (o.get("firstName", "") + " " + o.get("lastName", "")).strip() or o.get("email")
        oid = o["id"]
        n = c.count("0-136", [[OPEN, LIVE, {"propertyName": "hubspot_owner_id",
                                            "operator": "EQ", "value": oid}]])
        if n: out.append(("leaver", f"{n} open lead(s) still owned by {nm}, deactivated"))
        d = c.count("deals", [[{"propertyName": "hubspot_owner_id", "operator": "EQ", "value": oid},
                               {"propertyName": "hs_is_closed", "operator": "EQ", "value": "false"}]])
        if d: deals += d; who.append((nm, d))
        co = c.count("companies", [[{"propertyName": "hubspot_owner_id",
                                     "operator": "EQ", "value": oid}]])
        if co: backlog += co; people += 1
    if deals:
        out.append(("leaver deals", f"{deals} open deal(s) held by {len(who)} deactivated users"))
        c.note("Open deals by deactivated owner: " +
               ", ".join(f"{n} ({d})" for n, d in sorted(who, key=lambda x: -x[1])))
    if backlog:
        out.append(("backlog", f"{backlog:,} companies owned by {people} deactivated "
                               f"users - known backlog, not new"))

    n = c.count("deals", [[{"propertyName": "createdate", "operator": "GTE", "value": LAUNCH},
                           {"propertyName": "pipeline", "operator": "EQ", "value": "default"},
                           {"propertyName": "num_associated_contacts", "operator": "EQ", "value": "0"}]])
    if n: out.append(("deals", f"{n} new-business deal(s) since launch with no contact"))

    for prop, obj in (("trigger_lead_reassignment", "companies"),
                      ("trigger_multithread_alert", "companies"),
                      ("trigger_unowned_lead_routing", "contacts")):
        try:
            n = c.count(obj, [[{"propertyName": prop, "operator": "HAS_PROPERTY"}]])
        except Exception: continue
        if n: out.append(("stuck trigger",
                          f"{n} {obj[:-1]} record(s) with {prop} set - second workflow did not run"))

    # events. Compare against the participation records, never against the marketing
    # event's registrants/attendees fields - those are integration counters and run high.
    me, after = [], None
    while True:
        u = "/marketing/v3/marketing-events/?limit=100" + (f"&after={after}" if after else "")
        try: r = c.api(u)
        except Exception: break
        me += r.get("results", [])
        after = r.get("paging", {}).get("next", {}).get("after")
        if not after: break
    events = c.page("0-162", ["hs_name", "marketing_event_id",
                              "total_registrations", "total_attendees"])
    linked = {e["properties"].get("marketing_event_id"): e for e in events
              if e["properties"].get("marketing_event_id")}

    orphaned = [m for m in me if str(m.get("objectId")) not in linked
                and ((m.get("registrants") or 0) > 0 or (m.get("attendees") or 0) > 0)]
    if orphaned:
        out.append(("events", f"{len(orphaned)} marketing event(s) with people but no event "
                              f"record - invisible to attribution"))
        for m in orphaned[:10]:
            c.note(f"No event record: {m.get('eventName','')[:60]}")

    sr = sa = sn = 0
    for mid, e in linked.items():
        p = e["properties"]
        tr = int(float(p.get("total_registrations") or 0))
        ta = int(float(p.get("total_attendees") or 0))
        try: want = wanted_labels(c, mid)
        except Exception: continue
        wr = len(want)
        wa = sum(1 for v in want.values() if LBL_ATT in v)
        if wr > tr or wa > ta:
            sn += 1; sr += max(wr - tr, 0); sa += max(wa - ta, 0)
            repairable.append((e["id"], mid, p.get("hs_name", "")))
            c.note(f"Short on {p.get('hs_name','')[:52]}: {tr}/{wr} registered, {ta}/{wa} attended")
    if sn:
        out.append(("events", f"{sn} event(s) out of sync - {sr} registrant(s) and "
                              f"{sa} attendee(s) missing"))
    return out, repairable


def repair(c, target):
    """Create missing Registered/Attended associations. Returns (reg, att, failures).

    A v4 association PUT REPLACES the label set for a pair, so the desired set must
    include everything already there - Net new included - or it gets stripped.
    """
    event_id, mid, _ = target
    want = wanted_labels(c, mid)
    cur = current_labels(c, event_id)
    added_r = added_a = 0
    failed = []
    for cid, need in want.items():
        have = cur.get(cid, set())
        if need <= have: continue
        body = [{"associationCategory": "USER_DEFINED", "associationTypeId": t}
                for t in sorted(have | need)]
        try:
            c.api(f"/crm/v4/objects/0-162/{event_id}/associations/0-1/{cid}", body, method="PUT")
            if LBL_REG in need - have: added_r += 1
            if LBL_ATT in need - have: added_a += 1
        except Exception as e:
            failed.append(f"{cid}: {e}")
    if added_r or added_a:
        try:  # nudge net new tagging and deal attribution to recompute
            c.api(f"/crm/v3/objects/0-162/{event_id}",
                  {"properties": {"run_deal_attribution": "true"}}, method="PATCH")
        except Exception:
            pass
    return added_r, added_a, failed
