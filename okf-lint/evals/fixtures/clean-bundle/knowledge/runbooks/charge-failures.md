---
type: Runbook
title: Charge failures
description: Triage elevated charge failure rates.
tags: [oncall, payments]
timestamp: 2026-06-12T14:00:00Z
---

# Trigger

Alert fires when the failure rate on the [Charge API](/apis/charge.md)
exceeds 5% over 10 minutes.

# Steps

1. Check the processor status page for an upstream outage.
2. Compare failure codes: a spike in `card_declined` is usually organic;
   `processor_error` points at the integration.
3. If the processor is down, enable the fallback processor and announce in
   the incident channel.
