---
type: BigQuery Table
title: Refunds
description: One row per refund event issued against an order.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=refunds
tags: [sales, refunds]
timestamp: 2026-06-18T00:00:00Z
---

# Schema

| Column        | Type      | Description                              |
|---------------|-----------|------------------------------------------|
| `refund_id`   | STRING    | Unique refund identifier.                |
| `order_id`    | STRING    | The refunded [order](/tables/orders.md). |
| `amount_usd`  | NUMERIC   | TODO confirm whether this is net of fees |

# Examples

# Notes

Partial refunds produce multiple rows per order.
