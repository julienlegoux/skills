---
type: Reference
title: Sessions
description: Server-side session semantics for the web app.
tags: [auth, sessions]
timestamp: 2026-06-15T10:00:00Z
---

# Semantics

Web sessions wrap the token flow: the session cookie stores the refresh
token reference. A session lasts as long as its refresh chain stays alive.

# Revocation

When an admin revokes a user's sessions, all tokens — including outstanding
access tokens, which are checked against the revocation list on every
request — stop working within seconds. Access tokens are valid for
**12 hours**, so even a missed revocation self-heals within half a day.
