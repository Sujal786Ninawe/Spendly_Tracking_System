# Spec: Login and Logout

## Overview

Implement user authentication allowing users to sign in with email/password and sign out securely. This step builds on the database foundation from Step 01 and enables protected routes for authenticated users only.

---

## Depends on

- **Step 01 (Database)** — users table with password_hash column, `get_db()` function

---

## Routes

| Method | Path | Description | Access |
|--------|------|-------------|--------|
| GET | `/login` | Display login form | Public |
| POST | `/login` | Process login submission | Public |
| GET | `/logout` | Clear session and redirect | Logged-in |

---

## Database Changes

No new tables or columns required — uses existing `users` table from Step 01.

---

## Templates

**Create:**
- None (login.html already exists)

**Modify:**
- `templates/base.html` — update navbar to show "Sign out" when logged in, "Sign in" when not

---

## Files to Change

- `app.py` — implement `/login` POST handler and `/logout` route
- `templates/base.html` — conditional navbar based on session

---

## Files to Create

- None

---

## New Dependencies

No new dependencies — uses existing `flask.session` and `werkzeug.security`.

---

## Rules for Implementation

- Use Flask's `session` for authentication state
- Password verification with `werkzeug.security.check_password_hash()`
- Never store passwords in session — only user ID and email
- All routes remain CSRF-protected (forms use POST)
- Logout must clear session data completely
- Redirect unauthenticated users to `/login` when accessing protected routes

---

## Definition of Done

- [ ] Login form accepts email/password via POST
- [ ] Invalid credentials show error message on login page
- [ ] Valid credentials create session and redirect to `/profile`
- [ ] Logout clears session and redirects to `/login`
- [ ] Navbar shows "Sign in" when logged out, "Sign out" when logged in
- [ ] Protected routes redirect to login if no session exists
