---
type: Reference
title: Rate limits
description: Request quotas for the identity APIs.
tags: [limits, quotas]
timestamp: 2026-06-20T10:00:00Z
---

# Quotas

| Endpoint            | Limit                        |
|---------------------|------------------------------|
| `POST /v1/token`    | 60 requests/min per client   |
| `POST /v1/refresh`  | 60 requests/min per client   |
| `GET  /v1/userinfo` | 600 requests/min per client  |

Exceeding a quota returns `429` with a `Retry-After` header. Because
refresh tokens are reusable for up to five refreshes, clients hitting the
refresh quota can safely retry with the same token after backing off.
