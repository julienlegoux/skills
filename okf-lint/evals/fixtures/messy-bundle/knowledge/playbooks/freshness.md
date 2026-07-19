---
type: playbook
title: Freshness alert
description: Triage a data freshness alert on the orders pipeline.
tags: [oncall, incident]
timestamp: 2026-05-01T00:00:00Z
---

# Trigger

The freshness SLA for [orders](/tables/orders.md) is 30 minutes; an alert
fires as soon as the table breaches it.

# Steps

1. Check the ingestion job dashboard.
2. If the job is stuck, restart it and note the incident in the log.
3. Escalate to the pipeline owner if lag exceeds 2 hours.
