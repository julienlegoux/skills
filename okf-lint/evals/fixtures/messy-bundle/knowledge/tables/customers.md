---
type: BigQuery Table
title: Customers
description: One row per registered customer account.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=customers
tags: [Sales, crm]
timestamp: 2026-05-20T00:00:00Z
---

# Schema

| Column        | Type      | Description                              |
|---------------|-----------|------------------------------------------|
| `customer_id` | STRING    | Globally unique customer identifier.     |
| `email`       | STRING    | Primary contact email, lowercased.       |
| `created_at`  | TIMESTAMP | Account creation time.                   |

# Joins

To attach order history, join to [orders](/tables/orders.md) using the
`email` column, which is the stable identifier shared by both tables. Note
that `orders.total_usd` is stored as FLOAT64, so cast before exact
comparisons.
