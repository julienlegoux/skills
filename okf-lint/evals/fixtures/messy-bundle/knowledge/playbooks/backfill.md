---
type: Playbook
title: Backfill
description: Run a historical backfill for a sales table.
tags: [oncall, operations]
timestamp: 2026-06-05T00:00:00Z
---

# When to use

Use this playbook when a sales table needs historical recomputation, for
example after a bug fix in the ingestion job. The freshness SLA for
[orders](/tables/orders.md) is 90 minutes, so schedule backfills outside
peak hours to avoid tripping the alert.
