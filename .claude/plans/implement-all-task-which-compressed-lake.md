# Profile Page Implementation Plan

## Context

This plan implements the profile page feature (Spec 04) for the Spendly expense tracker. Users need the ability to view and edit their account information (name, email, password) after logging in. The feature builds on the existing authentication system from Step 02 and uses the existing `users` table from Step 01.

---

## Implementation Approach

### 1. Create Profile Template (`templates/profile.html`)

Create a new template with two sections:
- **Edit Profile Section**: Form to update name and email
- **Change Password Section**: Form to change password with current password verification

**Styling**: Use existing CSS classes from auth templates (`auth-section`, `auth-card`, `form-group`, `form-input`, `btn-submit`, `auth-error`) plus a new `success-message` class for feedback.

**Template Structure**:
- Extend `base.html`
- Display success/error messages via query params or flashed messages
- Two separate POST forms (profile update + password change)
- Pre-populate inputs with current user data from `session`

---

### 2. Implement Route Handlers (`app.py`)

Add three route handlers:

#### GET `/profile` (Lines ~165-180)
- Check session for `user_id`, redirect to `/login` if not authenticated
- Fetch current user data from database
- Render `profile.html` with user's current name and email

#### POST `/profile` (Lines ~182-220)
- Validate session
- Extract `name` and `email` from form
- Validate: name min 2 chars, email valid format, email unique (query existing users)
- On success: UPDATE users table, update `session["email"]`, flash success message
- On error: flash error message, re-render profile with current values

#### POST `/profile/change-password` (Lines ~222-260)
- Validate session
- Extract `current_password`, `new_password`, `confirm_password`
- Validate: current password matches hash (use `check_password_hash`)
- Validate: new password min 8 characters
- Validate: confirm password matches new password
- On success: UPDATE password_hash, flash success message
- On error: flash appropriate error message

---

### 3. Add Success/Error Message Styling

Add CSS classes to `static/css/style.css`:
- `.success-message` - green background for success feedback
- `.auth-error` already exists for errors

---

### 4. Verification

After implementation:
1. Start the app: `python app.py`
2. Login with a test user
3. Navigate to `/profile` - verify current data displays
4. Update name/email - verify success message and persistence
5. Try duplicate email - verify error message
6. Change password with correct current password - verify success
7. Change password with wrong current password - verify error
8. Logout, then try accessing `/profile` - verify redirect to login

---

## Files to Modify

| File | Action | Purpose |
|------|--------|---------|
| `templates/profile.html` | Create | Profile UI with edit forms |
| `app.py` | Modify | Add GET /profile, POST /profile, POST /profile/change-password routes |
| `static/css/style.css` | Modify | Add success message styling |

---

## Critical Implementation Details

- Use `werkzeug.security.generate_password_hash` and `check_password_hash`
- Session keys: `session["user_id"]` and `session["email"]`
- Email uniqueness check: `SELECT id FROM users WHERE email = ? AND id != ?`
- All routes protected with session check redirecting to `url_for("login")`
- Form methods: POST with CSRF protection (Flask WTF if available, otherwise basic)
- Flash messages for feedback: `flash("Profile updated successfully", "success")`
