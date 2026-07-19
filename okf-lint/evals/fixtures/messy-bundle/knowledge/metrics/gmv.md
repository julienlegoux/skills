---
type: Metric
title: GMV
description: Gross merchandise value definition.
tags: [revenue, finance]
timestamp: 2027-01-01T00:00:00Z
---

# Definition

GMV is computed as the sum of `total_usd` over all rows of the
[orders table](/tables/orders.md), **including cancelled orders**, since
cancellations still represent demand.

```sql
SELECT SUM(total_usd) FROM sales.orders;
```
