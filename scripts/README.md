# scripts

Health checks that keep the vault honest and current. Plain Python 3, no dependencies.

    python3 run.py usecure          read only
    python3 run.py usecure --fix    repair what is safely repairable
    python3 run.py --all            every client in clients/

Exit 0 clean, 1 findings, 2 could not run.

## Shape

| File | What it is |
|---|---|
| `run.py` | entry point - loads a client module, runs it, writes the note, posts to Slack |
| `lib.py` | everything generic: HubSpot API, metric writeback, Check note, lint runner, Slack |
| `lint.py` | vault conventions - client-agnostic, runs as part of every check |
| `clients/<name>.py` | **only** what is true of that client: what to count, what to check |

A client module exports `NAME`, `TOKEN_ENV`, `metrics(c)` and a `check` registry, and
optionally `repair(c, target)`. Everything else is inherited, so a fix to the writeback
logic lands for every client at once rather than in one copy of five.

## Adding a check

One decorated function. Nothing else changes - it is picked up, run, counted and reported
automatically.

```python
@check("Every renewal has an owner")
def _renewal_owners(c):
    n = c.count("deals", [[{"propertyName": "pipeline", "operator": "EQ", "value": RENEWAL},
                           {"propertyName": "hubspot_owner_id", "operator": "NOT_HAS_PROPERTY"}]])
    return [f"{n} renewal(s) with no owner"] if n else []
```

Return a list of finding strings, or `[]` when clean. The name is what appears in Slack and
in the Check note, so write it as the thing that should be true.

For a check that can repair what it finds, add `repairs=True` and return
`(findings, targets)`; `run.py --fix` passes each target to the module's `repair()`.

**Every check runs independently.** One raising an exception never hides the others, and a
check that fails to run is reported as **could not run, result unknown** - not silently
counted as a pass. That distinction is the whole point: a monitor you cannot tell apart
from a broken monitor is worth nothing.

## Adding a client

1. Copy `clients/usecure.py` and strip it back to that client's metrics and checks -
   most of it is `@check` functions you either keep, adapt or delete
2. Set its token env var
3. Make sure `Clients/<Name>/Metrics/` has a note per metric, named exactly as the key
   returned by `metrics()` - that is how the writeback finds them
4. `python3 run.py <name>`

Metric notes that do not exist are reported rather than created silently, so a typo in a
metric name shows up as a finding instead of disappearing.

## What it writes

- `value:` and `verified:` on each metric note
- a dated note in `Clients/<Name>/Checks/`
- with `--fix`, association labels in HubSpot - and it always reports what it repaired
  rather than quietly tidying up, so an upstream fault stays visible

## Environment

    USECURE_HUBSPOT_TOKEN     per client, named in the client module
    TJM_SLACK_WEBHOOK         monitoring channel
    VAULT_PATH                defaults to the repo root

Never commit either. `.gitignore` blocks `.env`.
