# User Management Web App

Project flow:
- `app.py` initializes the SQLite database (creates `users` table if missing) and starts a small Flask app.
- The `/` route handles GET (renders users) and POST (adds a new user then redirects).

Tech stack:
- Python, Flask
- SQLite
- HTML/CSS (Jinja2 templates)

Run locally:
1. Create a virtualenv and install requirements:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
2. Run the app:
```
python app.py
```
3. Open http://127.0.0.1:5000/
