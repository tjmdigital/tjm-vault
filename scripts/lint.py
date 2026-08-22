"""Vault lint - protects the conventions the derived views depend on.

The whole system rests on frontmatter being right. One typo in waiting_on and an
item silently vanishes from Now, with no error. This catches that.

Exit 0 = clean, 1 = problems found.
"""
import os, re, sys, collections, datetime

VAULT = os.environ.get("VAULT_PATH", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Obsidian does not resolve a wikilink inside code, and neither should we. Without
# this, documentation that shows the syntax reads as a link to a note called "that
# note", and every note carrying that boilerplate adds a phantom broken link.
CODE = re.compile(r"^```.*?^```|`[^`\n]*`", re.S | re.M)
SKIP = (".git", ".obsidian", "Templates", "scripts")
TYPES = {"system","issue","metric","decision","workflow","property","check",
         "meeting","person","pattern","platform","client"}
EXEMPT = ("00 ", "Now", "Today", "README", "Patterns/Patterns", "Platform/Platform")

def notes():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith(".md"):
                yield os.path.relpath(os.path.join(root, f), VAULT)

def fm(rel):
    s = open(os.path.join(VAULT, rel)).read()
    if not s.startswith("---"): return {}, s
    return ({k.strip(): v.strip() for k, v in
             (l.split(":", 1) for l in s.split("---")[1].split("\n")
              if ":" in l and not l.startswith(" "))}, s)

def main():
    paths = list(notes())
    names = {os.path.splitext(os.path.basename(p))[0]: p for p in paths}
    problems = []

    # duplicate filenames make every wikilink to them ambiguous
    c = collections.Counter(os.path.basename(p) for p in paths)
    for f, n in c.items():
        if n > 1:
            problems.append(("ambiguous", f"{n} notes named {f} - wikilinks to it resolve unpredictably"))

    inbound = collections.defaultdict(set)
    for p in paths:
        _, s = fm(p)
        for m in re.findall(r"\[\[([^\]|#]+)", CODE.sub("", s)):
            m = m.strip()
            if not m: continue
            if m in names: inbound[m].add(p)
            else: problems.append(("broken link", f"{p} -> [[{m}]]"))

    today = datetime.date.today()
    for p in paths:
        f, s = fm(p)
        t = f.get("type")
        if p.startswith(EXEMPT): continue
        if not t:
            problems.append(("no type", p)); continue
        if t not in TYPES:
            problems.append(("bad type", f"{p} has type: {t}"))
        if t in ("system","metric","decision","workflow","property","check","meeting") \
           and not f.get("client"):
            problems.append(("no client", p))
        if t == "system" and not f.get("pattern"):
            problems.append(("system without pattern", f"{p} - if it is not a build, type it as issue"))
        # a person must be a wikilink, or Now silently drops it
        w = f.get("waiting_on")
        if w and "[[" not in w:
            problems.append(("waiting_on not a link", f"{p} - {w}"))
        if w and not w.startswith("["):
            problems.append(("waiting_on not a list", f"{p} - length() is unreliable on a bare string"))
        if (f.get("waiting_on") or f.get("blocked_by")) and not f.get("since"):
            problems.append(("no since", f"{p} - the day counter will not work"))
        # decay
        v = f.get("verified")
        if v:
            try:
                age = (today - datetime.date.fromisoformat(v)).days
                limit = int(f.get("decays", 14))
                if age > limit:
                    problems.append(("stale", f"{p} - verified {age} days ago, decays at {limit}"))
            except ValueError:
                problems.append(("bad date", f"{p} - verified: {v}"))

    for n, p in names.items():
        if p.startswith(EXEMPT) or "/" not in p: continue
        f, _ = fm(p)
        if f.get("automated") == "true": continue   # surfaced by Dataview, never linked
        if not inbound.get(n):
            problems.append(("orphan", f"{p} - nothing links to it"))

    if not problems:
        print(f"vault lint: clean ({len(paths)} notes)"); return 0
    by = collections.defaultdict(list)
    for k, v in problems: by[k].append(v)
    print(f"vault lint: {len(problems)} problem(s) across {len(paths)} notes\n")
    for k in sorted(by):
        print(f"{k} ({len(by[k])})")
        for v in by[k][:12]: print(f"   {v}")
        if len(by[k]) > 12: print(f"   ... and {len(by[k])-12} more")
        print()
    return 1

if __name__ == "__main__":
    sys.exit(main())