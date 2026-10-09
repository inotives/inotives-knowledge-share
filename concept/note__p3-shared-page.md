---
title: P3 shared test page
description: Dummy page that two contributors edit, to test merges and conflicts.
type: note
status: draft
owner: "inotives-inoai"
created_at: 2026-10-09
created_by: "inotives-inoai"
ai_assisted: false
human_reviewed: false
tags: []
---

# P3 shared test page

## Section A: orders

- An order is one checkout by one customer.
- An order has one or more items.
- Refunds are tracked in the refunds table, one row per refund.

## Section B: customers

- A customer is one account.
- An active customer has ordered in the last 90 days.
- Guest checkouts have an empty customer id and are not counted as customers.

## Section C: reports

- The daily report runs at 06:00.
- It reads the orders table.
- Late rows appear in the next day's report.
