---
type: platform
verified: 2026-08-19
---
# Association type IDs

Primary vs unlabelled matters enormously - using the unlabelled one gives you
"any of", which is rarely what you want.

| From | To | Type ID |
|---|---|---|
| Contact | Company (**Primary**) | `1` |
| Contact | Company (unlabelled) | `279` |
| Lead | Contact (**Primary**) | `578` |
| Lead | Contact (unlabelled) | `608` |
| Lead | Company (**Primary**) | `580` |
| Lead | Company (unlabelled) | `610` |
| Contact | Lead | `609` |
| Deal | Company (**Primary**) | `5` |
| Company | Deal | `6` / `342` |
| Deal | Contact | `3` |

**Where this bit:** building a list of contacts at non-paying partner companies using
typeId `279` let a paying partner through, because a contact with two companies matched
on the wrong one. Switching to `1` fixed it.
