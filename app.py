from flask import Flask, render_template, request, redirect, url_for, session
from database.db import get_db, init_db, seed_db
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"

# Initialize database on startup
with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate password length
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters")

        conn = get_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template("register.html", error="Email already registered")

        # Hash password and insert new user
        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                       (name, email, password_hash))
        conn.commit()

        # Get the new user's ID
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        # Auto-login: create session
        session["user_id"] = user["id"]
        session["email"] = email

        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(f"Login attempt - Email: {email}")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            print(f"User found: {user['email']}")
            if check_password_hash(user["password_hash"], password):
                print("Password matched!")
                session["user_id"] = user["id"]
                session["email"] = user["email"]
                return redirect(url_for("dashboard"))
            else:
                print("Password mismatch!")
        else:
            print("User not found!")

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    # Get user info
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (session["user_id"],))
    user = cursor.fetchone()

    # Get all expenses for this user
    cursor.execute("""
        SELECT id, amount, category, date, description
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, (session["user_id"],))
    expenses = cursor.fetchall()

    # Calculate total amount
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) as total
        FROM expenses
        WHERE user_id = ?
    """, (session["user_id"],))
    total_amount = cursor.fetchone()["total"]

    # Get category breakdown
    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
    """, (session["user_id"],))
    categories = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html",
                         user=user,
                         expenses=expenses,
                         total_amount=total_amount,
                         categories=categories)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    # Get current user data
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (session["user_id"],))
    user = cursor.fetchone()
    conn.close()

    # Handle POST request - update profile
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        # Validate name
        if not name or len(name) < 2:
            return render_template("profile.html", user=user, error_message="Name must be at least 2 characters")

        # Validate email format
        if not email or "@" not in email:
            return render_template("profile.html", user=user, error_message="Invalid email address")

        # Check for duplicate email (excluding current user)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ? AND id != ?", (email, session["user_id"]))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return render_template("profile.html", user=user, error_message="Email already registered")

        # Update user profile
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, session["user_id"]))
        conn.commit()
        conn.close()

        # Update session
        session["email"] = email

        return render_template("profile.html", user={"name": name, "email": email}, success_message="Profile updated successfully")

    return render_template("profile.html", user=user)


@app.route("/profile/change-password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        return redirect(url_for("login"))

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    # Get current user data
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
    user = cursor.fetchone()

    # Validate current password
    if not check_password_hash(user["password_hash"], current_password):
        cursor.execute("SELECT name, email FROM users WHERE id = ?", (session["user_id"],))
        profile_user = cursor.fetchone()
        conn.close()
        return render_template("profile.html", user=profile_user, error_message="Current password is incorrect")

    # Validate new password length
    if len(new_password) < 8:
        cursor.execute("SELECT name, email FROM users WHERE id = ?", (session["user_id"],))
        profile_user = cursor.fetchone()
        conn.close()
        return render_template("profile.html", user=profile_user, error_message="New password must be at least 8 characters")

    # Validate passwords match
    if new_password != confirm_password:
        cursor.execute("SELECT name, email FROM users WHERE id = ?", (session["user_id"],))
        profile_user = cursor.fetchone()
        conn.close()
        return render_template("profile.html", user=profile_user, error_message="New passwords do not match")

    # Update password
    password_hash = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, session["user_id"]))
    conn.commit()
    conn.close()

    return render_template("profile.html", user=user, success_message="Password updated successfully")


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
