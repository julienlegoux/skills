---
type: API Endpoint
title: Charge API
description: Create and capture a card charge.
resource: https://api.acmepay.example/v1/charges
tags: [payments, api]
timestamp: 2026-07-01T09:00:00Z
---

# Behavior

`POST /v1/charges` creates a charge. Requests carrying an
`Idempotency-Key` header are deduplicated for 24 hours: retries with the
same key return the original response. Rate limit is 100 requests per
minute per API key.

# Examples

```bash
curl -X POST https://api.acmepay.example/v1/charges \
  -H "Idempotency-Key: 9f3a" -d amount=1200 -d currency=usd
```

Failed charges can be retried; captured charges are reversed via the
[Refund API](/apis/refund.md).
