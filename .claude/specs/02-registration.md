# Spec: User Registration

## Overview

Implement user registration allowing new users to create an account with name, email, and password. This builds on the database foundation from Step 01.

---

## Depends on

- **Step 01 (Database)** — users table with password_hash column, `get_db()` function

---

## Routes

| Method | Path | Description | Access |
|--------|------|-------------|--------|
| GET | `/register` | Display registration form | Public |
| POST | `/register` | Process registration submission | Public |

---

## Database Changes

No new tables or columns required — uses existing `users` table from Step 01.

---

## Templates

**Create:**
- `templates/register.html` — registration form with name, email, password fields

**Modify:**
- None (base.html already has auth-section styles)

---

## Files to Change

- `app.py` — implement `/register` GET/POST handlers

---

## Files to Create

- `templates/register.html`

---

## New Dependencies

No new dependencies — uses existing `flask` and `werkzeug.security`.

---

## Rules for Implementation

- Password must be at least 8 characters
- Email must be unique — show error if already registered
- Hash passwords using `werkzeug.security.generate_password_hash()`
- Never store plain text passwords
- On successful registration, auto-login the user (create session)
- Redirect to `/dashboard` after successful registration
- Form submissions use POST with CSRF protection

---

## Registration Form Fields

| Field | Type | Validation |
|-------|------|------------|
| name | text | Required, min 2 characters |
| email | email | Required, valid format, unique |
| password | password | Required, min 8 characters |

---

## Definition of Done

- [ ] Registration form displays with name, email, password fields
- [ ] POST to `/register` creates new user with hashed password
- [ ] Duplicate email shows error message
- [ ] Password under 8 characters shows error
- [ ] Successful registration creates session and redirects to `/dashboard`
- [ ] Authenticated users redirected away from `/register`
