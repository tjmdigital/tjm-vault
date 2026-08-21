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

## Requires

- [Dataview](https://github.com/blacksmithgu/obsidian-dataview) - most queries need it
- [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) - [[Today]] needs it
- [Obsidian Git](https://github.com/Vinzent03/obsidian-git) - pull on open, push on change
