#!/usr/bin/env python3
"""Run a client health check.

    python3 run.py usecure            read only
    python3 run.py usecure --fix      repair what is safely repairable
    python3 run.py --all              every client module in clients/

Exit 0 = clean, 1 = findings, 2 = could not run.
"""
import os, sys, datetime, importlib, pkgutil
import lib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def available():
    d = os.path.join(HERE, "clients")
    return sorted(m.name for m in pkgutil.iter_modules([d]) if not m.name.startswith("_"))


def run(mod_name, fix=False):
    mod = importlib.import_module(f"clients.{mod_name}")
    c = lib.Client(mod.NAME, mod.TOKEN_ENV,
                   portal=getattr(mod, "PORTAL", None),
                   launch=getattr(mod, "LAUNCH", None))
    today = datetime.date.today().isoformat()
    label = f"*{mod.NAME} - weekly health check*"

    if not c.token:
        lib.slack(f":rotating_light: {label}\n`{mod.TOKEN_ENV}` is not set, so nothing ran.")
        print(f"{mod.TOKEN_ENV} is not set", file=sys.stderr)
        return 2
    try:
        m = mod.metrics(c)
    except Exception as e:
        lib.slack(f":rotating_light: {label}\nCould not read HubSpot: `{e}`. "
                  f"The result is unknown, not clear.")
        print("could not read HubSpot:", e, file=sys.stderr)
        return 2

    moved = {}
    for k, v in m.items():
        if k.startswith("_"): continue
        old = c.update_metric(k, v, today)
        if old: moved[k] = old
    missing = [k for k, v in moved.items() if v == "MISSING"]

    results, findings, repairable = mod.check.run(c)

    if fix and repairable and hasattr(mod, "repair"):
        tr = ta = 0; failures = []
        for _name, target in repairable:
            r, a, f = mod.repair(c, target)
            tr += r; ta += a; failures += f
            if r or a: c.note(f"Repaired {target[2][:52]}: +{r} registered, +{a} attended")
        if tr or ta:
            findings = [x for x in findings if "out of sync" not in x[1]]
            results = [(n, "repaired" if "sync" in n else s_, e) for n, s_, e in results]
            findings.append(("Repaired", f"{tr} registrant and {ta} attendee association(s) "
                                         f"across {len(repairable)} event(s)"))
        if failures:
            findings.append(("Repair failed", f"{len(failures)} could not be created"))
            for f in failures[:10]: c.note(f)

    lint_rc, lint_out = lib.run_lint()
    lib.write_check(c, today, m, moved, results, findings, lint_out)

    unknown = [n for n, s_, _ in results if s_ == "UNKNOWN"]
    passed  = [n for n, s_, _ in results if s_ in ("pass", "repaired")]
    clean = not findings and lint_rc == 0 and not missing and not unknown

    icon = ":white_check_mark:" if clean else (":rotating_light:" if unknown else ":warning:")
    txt = f"{icon} {label}\n{m.get('_headline','')}\n"
    for cat, msg in findings: txt += f"• {cat}: {msg}\n"
    for k in missing: txt += f"• Vault: no metric note for {k}\n"
    if lint_rc == 1:
        txt += f"• Vault lint: {lint_out.splitlines()[0] if lint_out else 'problems found'}\n"
    for n in unknown:
        txt += f"• :grey_question: {n} - could not run, result unknown not clear\n"
    # always say what was checked, so a silent check is distinguishable from a clean one
    txt += (f"_{len(passed)}/{len(results)} checks passed"
            + (f", {len(unknown)} could not run" if unknown else "")
            + f". Passed: {', '.join(passed)}._" if passed or unknown else "")
    lib.slack(txt.rstrip())
    print(txt)
    for k, v in m.items():
        if not k.startswith("_"):
            print(f"  {k}: {v}" + (f"  (was {moved[k]})" if moved.get(k) not in (None, "MISSING") else ""))
    print(f"\n{lint_out}")
    return 0 if clean else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fix  = "--fix" in sys.argv
    names = available() if "--all" in sys.argv else args
    if not names:
        print(f"usage: run.py <client> [--fix] | --all\navailable: {', '.join(available())}")
        return 2
    worst = 0
    for n in names:
        if n not in available():
            print(f"no client module called {n}", file=sys.stderr); worst = max(worst, 2); continue
        worst = max(worst, run(n, fix))
    return worst


if __name__ == "__main__":
    sys.exit(main())
