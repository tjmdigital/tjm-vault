# TJM vault

Working knowledge for TJM Digital's RevOps engagements. Obsidian vault, git-backed.

## Why it is shaped this way

Almost every mistake worth avoiding in this work has been a **decay** problem: a claim
that was true when written and false when repeated. A metric definition that changed.
A rotation pool that had someone in it who had left. A count taken in July and quoted
in August.

So every factual note carries `verified:` and `decays:` in its frontmatter, and the
dashboard surfaces anything that has gone stale. The vault nags; you do not have to remember.

## Layout

| Folder | What lives there |
|---|---|
| `Platform/` | Client-agnostic facts about HubSpot. API gotchas, limits, behaviour. |
| `Patterns/` | Reusable mechanisms. Each one lists every client that has an implementation. |
| `Clients/<name>/` | One folder per client: Systems, Metrics, Decisions, HubSpot, Checks, Meetings, People. |
| `Templates/` | Note templates. Use them - the frontmatter is what makes the queries work. |

## Pages to know

- **[[Today]]** - work with a date on it, across every client. Needs the Tasks plugin.
- **[[Now]]** - what is stuck, on whom, and for how long. Derived, never maintained by hand.
- **[[00 Dashboard]]** - the wider view: freshness, hardcoded people, pattern reuse.
- **[[Patterns]]** - reusable mechanisms and where each is built.
- **[[Platform]]** - API facts and gotchas. Check before trial and error.
- **[[Usecure]]** - the client index.

## Naming

Where a client's implementation shares a name with its pattern, the client note takes a
suffix: `Stale lead ladder` is the pattern, `Stale lead ladder (Usecure)` is the build.
Obsidian resolves wikilinks by filename alone, so two notes with the same name make every
link to either of them ambiguous.

**Tasks live inside the note that explains them**, as `- [ ] thing 📅 YYYY-MM-DD`, and surface
on [[Today]]. Putting them next to the context means picking one up cold costs nothing.

`Now` is state - what is stuck and on whom. `Today` is work - what has a date. A thing can be
on both.

## The one rule

A client `System` note must declare `pattern:` in its frontmatter. That single field is
what lets you open a pattern and see every time you have built it, what each client chose,
and what broke. Written at build time it costs five seconds. Extracted afterwards it never
happens at all.

## Secrets

Nothing secret goes in this repo. No API tokens, no portal passwords, no client credentials.
Notes refer to them by name (`USECURE_HUBSPOT_TOKEN`) and the values live in a local
gitignored `.env`.

## The weekly check

A scheduled cloud run every Wednesday at 15:00 UK, from `scripts/`. It needs nothing on
anyone's laptop - it clones this repo, runs, and pushes back.

```
scripts/run.py <client> [--fix]     one client
scripts/run.py --all                every module in scripts/clients/
scripts/lint.py                     conventions only, no API calls
```

Exit 0 clean, 1 findings, 2 could not run. **2 is not 0** - a check that could not run is
reported as unknown and never counted as a pass, because a broken check going quiet must
never read as a problem going away.

What one run does:

1. Re-counts every metric and writes `value:` and `verified:` back into its note
2. Runs each check independently, so one failing never hides the rest
3. Repairs what is safely repairable - currently missing event associations
4. Turns findings into issue notes under `Clients/<name>/Issues/`
5. Refreshes the `## Position` block on any note carrying `tracks_owner:`
6. Lints, writes a dated note to `Checks/`, commits, pushes, posts to Slack

### Issue notes

A finding written once a week is a log. An issue note is a memory: it carries `since`
(first seen), a history of every change in the number, and it sets `status: resolved` on
the run where the finding stops appearing. `Now` ages them off `since`.

Three fields decide whether one shows on `Now`:

| Field | Effect |
|---|---|
| `waiting_on` | moves it up into the human sections - it has a name against it now |
| `superseded_by` | a hand-written note already covers it; the count keeps updating, `Now` shows the other note |
| `status` | set to `resolved` by the run itself, never by hand |

If a problem clears and comes back, `since` resets to the return date, so the day counter
measures this spell rather than the original one. The history keeps both.

### Adding a check

One decorated function in the client module. Nothing else changes.

```python
@check("Every open lead has an owner")
def _unowned(c):
    n = c.count("0-136", [[OPEN, LIVE, NO_OWNER]])
    return [f"{n} open lead(s) with no owner"] if n else []
```

Return a list of strings, or `[]` when clean. Return `(message, markdown)` instead of a
string to attach a table the run keeps current on the issue note. Add `events=True` to the
decorator for a check that reports things that *happened* rather than things that are
*wrong* - those get reported but never become issue notes.

### Adding a client

One file in `scripts/clients/`, with `NAME`, `TOKEN_ENV`, a `metrics(c)` function and its
checks. `run.py --all` picks it up automatically.

### Where the numbers come from

Nothing quotes a count in prose and hopes. Metric notes are rewritten each run. Notes about
a person's records carry `tracks_owner:` and get a `## Position` table refreshed weekly -
Albir's note said 185 open deals when 104 were open and 77 had closed.

## Requires

- [Dataview](https://github.com/blacksmithgu/obsidian-dataview) - most queries need it
- [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) - [[Today]] needs it
- [Obsidian Git](https://github.com/Vinzent03/obsidian-git) - pull on open, push on change
