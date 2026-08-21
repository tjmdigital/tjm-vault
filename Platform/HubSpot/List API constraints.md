---
type: platform
verified: 2026-08-19
---
# List API constraints

- **Association filter branches only accept `IN_LIST`.** There is no `NOT_IN_LIST` at
  branch level, so exclusions need a separate suppression list referenced as a filter:
  ```json
  {"filterType": "IN_LIST", "operator": "NOT_IN_LIST", "listId": 3856}
  ```
  See [[Suppression list]].
- **`hs_list_size` reads null via the API.** Count `/memberships` instead.
- **Membership takes 60 to 100 seconds to populate** after a filter change. Verifying
  immediately gives a wrong answer.
- Property type matters: a string property needs `MULTISTRING`, not `ENUMERATION`, even
  when it looks like a dropdown.
- Rolling windows need `TIME_RANGED` with `IS_BETWEEN` and **both** endpoint behaviours
  set to `INCLUSIVE`. An `INDEXED` timepoint with a negative offset is rejected.
