---
type: platform
verified: 2026-08-21
---
# Notification recipients are UI-only

The in-app notification action (`0-8`) accepts `subject` and `body` through the API and
**silently drops any recipient field you send**. Read the flow back and only those two
keys are stored.

A workflow built entirely through the API therefore has a notification step that fires
into nothing. It will not error.

**Options:**
- Set the recipient once in the UI after building. Fine, but it is a manual step that
  must be remembered before switch-on.
- Use a **task** (`0-3`) instead, which *can* be assigned via API:
  ```json
  "owner_assignment": {"value": {"propertyName": "hubspot_owner_id", "type": "OBJECT_PROPERTY"}, "type": "CUSTOM"}
  ```
  A task is also trackable and sits on the record, which is usually better than a notification.
