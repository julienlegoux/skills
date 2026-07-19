---
type: API Endpoint
title: Refund API
description: Refund a captured charge, fully or partially.
resource: https://api.acmepay.example/v1/refunds
tags: [payments, api]
timestamp: 2026-06-10T09:00:00Z
---

# Behavior

`POST /v1/refunds` refunds a charge created by the
[Charge API](/apis/charge.md). Partial refunds are allowed until the full
captured amount is refunded. Refunds share the charge endpoints' rate limit
of 100 requests per minute per API key.

# Examples

```bash
curl -X POST https://api.acmepay.example/v1/refunds -d charge=ch_123 -d amount=600
```
