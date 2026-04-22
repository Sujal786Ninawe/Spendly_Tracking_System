# Spec: Dashboard Page

## Overview

Implement a dashboard page that displays an overview of the user's expenses with summary cards, category breakdown, and recent transactions. This builds on the authentication system from Step 02 and provides users with a visual summary of their spending.

---

## Depends on

- **Step 01 (Database)** — expenses table with amount, category, date columns
- **Step 02 (Login and Logout)** — session-based authentication, protected routes

---

## Routes

| Method | Path | Description | Access |
|--------|------|-------------|--------|
| GET | `/dashboard` | Display dashboard with expense summary | Logged-in |

---

## Database Changes

No new tables or columns required — uses existing `users` and `expenses` tables.

---

## Templates

**Create:**
- `templates/dashboard.html` — dashboard with summary cards, category breakdown, and expenses table

**Modify:**
- `templates/base.html` — add navbar link to "Dashboard" when logged in
- `static/css/style.css` — add dashboard-specific styles

---

## Files to Change

- `app.py` — implement `/dashboard` route with expense queries
- `templates/base.html` — add Dashboard link to navbar
- `static/css/style.css` — dashboard styling

---

## Files to Create

- `templates/dashboard.html`

---

## New Dependencies

No new dependencies — uses existing Flask and SQLite.

---

## Rules for Implementation

- Dashboard must be protected (redirect to `/login` if not authenticated)
- Use parameterized queries for all database access
- Calculate totals using SQL `SUM()` and `COUNT()` functions
- Group expenses by category for breakdown
- Order expenses by date (most recent first)
- Use CSS variables for colors — never hardcode hex values
- Dashboard should extend `base.html`
- Format currency with ₹ symbol

---

## Dashboard Components

| Component | Data Source | Description |
|-----------|-------------|-------------|
| Welcome message | users.name | Personalized greeting |
| Total spent | SUM(expenses.amount) | This month's total |
| Total transactions | COUNT(expenses.id) | Number of expenses |
| Categories used | COUNT(DISTINCT category) | Unique categories |
| Category breakdown | GROUP BY category | Amount per category |
| Recent expenses | SELECT * ORDER BY date | List of all expenses |

---

## Definition of Done

- [ ] GET `/dashboard` displays personalized welcome message
- [ ] Summary cards show total spent, transactions, and categories
- [ ] Category breakdown shows amount spent per category
- [ ] Recent expenses table lists all user's expenses
- [ ] Expenses ordered by date (newest first)
- [ ] Dashboard accessible only to logged-in users
- [ ] "Add Expense" button visible on dashboard
- [ ] Dashboard link in navbar when logged in
- [ ] Responsive design works on mobile and desktop

---

## UI Layout (dashboard.html)

```
+------------------------------------------+
|  Welcome back, [User]!                   |
|  Track your expenses and budget          |
+------------------------------------------+
|  [+ Add Expense Button]                  |
+------------------------------------------+
|  [Summary Cards Row]                     |
|  +-------------+ +-------------+ +-----+ |
|  | Total Spent | | Transactions| |Cat..| |
|  | ₹5,240      | | 24          | | 6   | |
|  +-------------+ +-------------+ +-----+ |
+------------------------------------------+
|  [By Category Section]                   |
|  - Food: ₹1,200                          |
|  - Transport: ₹450                       |
|  - Bills: ₹2,000                         |
+------------------------------------------+
|  [Recent Expenses Table]                 |
|  Date | Category | Description | Amount  |
|  ...                                     |
+------------------------------------------+
```
