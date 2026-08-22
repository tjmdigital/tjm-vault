# scripts

Two checks that keep the vault honest. Both are plain Python 3, no dependencies.

## `checks.py` - re-verifies Usecure against HubSpot

Pulls the live numbers, **writes them back** into `Clients/Usecure/Metrics/`
(`value:` and `verified:`), runs integrity checks on the builds, and writes a dated
note into `Clients/Usecure/Checks/`. Posts a summary to Slack if a webhook is set.

What it checks beyond the numbers:

- **Workflow state drift** - vault says a workflow is off, HubSpot says it is on
- Open leads with no owner
- Open leads owned by anyone who has been deactivated
- New-business deals since launch with no contact attached
- Two-stage trigger properties left set, which means a second workflow did not run
- Event-deal links with no Sourced/Influenced label

Exit 0 clean, 1 findings, 2 could not run.

## `lint.py` - protects the conventions

The derived views depend entirely on frontmatter being right, and a typo fails
silently rather than loudly. This catches broken links, ambiguous filenames, orphans,
missing `type`/`client`/`pattern`, `waiting_on` written as a bare string instead of a
list of links, missing `since`, and anything past its `decays` window.

Exit 0 clean, 1 problems.

## Environment

    USECURE_HUBSPOT_TOKEN    required by checks.py
    USECURE_SLACK_WEBHOOK    optional - posts the summary to #usecure-revops
    VAULT_PATH               defaults to the repo root

Never commit either secret. `.gitignore` blocks `.env`.

## Running them

    cd ~/dev/tjm-vault
    export USECURE_HUBSPOT_TOKEN=...
    python3 scripts/checks.py
    python3 scripts/lint.py
