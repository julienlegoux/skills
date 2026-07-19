---
type: Reference
title: Access tokens
description: Lifetime and refresh behavior of access tokens.
tags: [auth, tokens]
timestamp: 2026-07-05T10:00:00Z
---

# Lifetime

Access tokens are JWTs valid for **24 hours** from issuance. Clients should
refresh proactively at the 20-hour mark using the refresh endpoint. Refresh
tokens are single-use and rotate on every refresh.

# Revocation

Revoking a user's sessions via the admin console invalidates their refresh
tokens immediately; outstanding access tokens remain valid until expiry
because they are stateless. See [sessions](/auth/sessions.md).
