---
type: BigQuery Table
title: Orders
description: One row per completed customer order across all channels.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, orders]
timestamp: 2026-06-01T00:00:00Z
---

# Schema

| Column        | Type      | Description                              |
|---------------|-----------|------------------------------------------|
| `order_id`    | STRING    | Globally unique order identifier.        |
| `customer_id` | STRING    | Foreign key into [customers](/tables/customers.md). |
| `total_usd`   | NUMERIC   | Order total in US dollars.               |
| `placed_at`   | TIMESTAMP | When the customer submitted the order.   |

# Semantics

Cancelled orders are **excluded** from this table entirely; only completed
orders appear. Refunded orders remain, with the refund tracked separately in
[refunds](/tables/refunds.md).

# Joins

Joined with [customers](/tables/customers.md) on `customer_id`.
