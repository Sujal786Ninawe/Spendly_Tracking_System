# Spec: Profile Page

## Overview

Implement a user profile page where users can view and edit their account information. This builds on the authentication system from Step 02 and provides users with account management capabilities.

---

## Depends on

- **Step 01 (Database)** — users table with name, email, password_hash columns
- **Step 02 (Login and Logout)** — session-based authentication, protected routes

---

## Routes

| Method | Path | Description | Access |
|--------|------|-------------|--------|
| GET | `/profile` | Display profile page with user info | Logged-in |
| POST | `/profile` | Update profile information | Logged-in |
| POST | `/profile/change-password` | Change user password | Logged-in |

---

## Database Changes

No new tables or columns required — uses existing `users` table.

---

## Templates

**Create:**
- `templates/profile.html` — profile page with edit form and change password section

**Modify:**
- `templates/base.html` — ensure navbar has "Profile" link visible when logged in

---

## Files to Change

- `app.py` — implement `/profile` GET/POST handlers and `/profile/change-password` POST handler
- `templates/profile.html` — create profile UI with edit form

---

## Files to Create

- `templates/profile.html`

---

## New Dependencies

No new dependencies — uses existing `flask.session` and `werkzeug.security`.

---

## Rules for Implementation

- Profile page must be protected (redirect to `/login` if not authenticated)
- Current password required to change password
- New password must be at least 8 characters
- Email changes should validate uniqueness (no duplicate emails)
- Name and email updates should update session data
- Password change must use `generate_password_hash()`
- Success/error messages should be shown after form submissions
- Form submissions use POST with CSRF protection

---

## Profile Form Fields

| Field | Type | Validation |
|-------|------|------------|
| name | text | Required, min 2 characters |
| email | email | Required, valid format, unique |
| current_password | password | Required for password change |
| new_password | password | Min 8 characters, required for password change |
| confirm_password | password | Must match new_password |

---

## Definition of Done

- [ ] GET `/profile` displays user's current name and email
- [ ] POST `/profile` updates name and email with validation
- [ ] Duplicate email shows appropriate error message
- [ ] Password change requires current password verification
- [ ] New password must be at least 8 characters
- [ ] Confirm password must match new password
- [ ] Session data updated after profile changes
- [ ] Success message shown after successful update
- [ ] Profile link visible in navbar when logged in
- [ ] Unauthenticated users redirected to login

---

## UI Layout (profile.html)

```
+------------------------------------------+
|  Profile Settings                        |
+------------------------------------------+
|                                          |
|  [Edit Profile Section]                  |
|  - Name: [input]                         |
|  - Email: [input]                        |
|  - [Save Changes] button                 |
|                                          |
|  [Change Password Section]               |
|  - Current Password: [input]             |
|  - New Password: [input]                 |
|  - Confirm Password: [input]             |
|  - [Update Password] button              |
|                                          |
+------------------------------------------+
```
