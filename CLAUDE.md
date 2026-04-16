# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- **Backend**: Flask 3.1.3 with Werkzeug
- **Database**: SQLite (via `database/db.py`)
- **Testing**: pytest 8.3.5 with pytest-flask
- **Frontend**: Jinja2 templates with vanilla CSS/JS

## project Overview 
Spendly is the light weight expense tracker built with a flask and sqlite 

## Project Structure

```
expense-tracker/
├── app.py              # Flask application entry point
├── database/
│   ├── db.py           # Database utilities (get_db, init_db, seed_db)
│   └── __init__.py
├── templates/          # Jinja2 HTML templates
└── static/             # CSS and JavaScript assets
```

## Architecture

**Database Layer** (`database/db.py`):
- `get_db()` - Returns SQLite connection with `row_factory` and `foreign_keys` enabled
- `init_db()` - Creates tables using `CREATE TABLE IF NOT EXISTS`
- `seed_db()` - Inserts sample development data

**Routes** (`app.py`):
- Public: `/` (landing), `/register`, `/login`, `/terms`, `/privacy`
- Placeholder routes for future implementation: `/logout`, `/profile`, `/expenses/*`

**Templates**:
- `base.html` - Base template with navbar, footer, and Google Fonts (DM Serif Display, DM Sans)
- Auth templates use `{% extends "base.html" %}` with `auth-section`, `auth-card`, `form-group` classes
- Form submissions use POST to `/login` and `/register`

## Development Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py  # Runs on http://localhost:5001

# Run tests
pytest
pytest -v  # Verbose output
pytest tests/test_filename.py  # Single test file
pytest -k test_name  # Single test by name
```

## Implementation Notes

- Forms expect POST requests to `/login` and `/register`
- Error messages displayed via `{% if error %}` blocks in auth templates
- Static assets referenced at `static/css/style.css` and `static/js/main.js`
- App runs on port 5001 with debug mode enabled
