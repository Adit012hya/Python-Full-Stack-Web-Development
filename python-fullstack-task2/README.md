Authentication System - Task 2

User registration, login, logout with session-based authentication.

---

## Overview

Real web apps need secure user management. This project implements:
- User registration (signup)
- User login with password verification
- Session-based authentication
- Protected routes
- Secure logout

---

## Screenshots 
Registration:<img width="2068" height="1278" alt="Screenshot 2026-06-09 001818" src="https://github.com/user-attachments/assets/99b02844-57ba-4fa2-8956-1683d408de2b" />
Login: <img width="2074" height="1276" alt="Screenshot 2026-06-09 001839" src="https://github.com/user-attachments/assets/c1213c99-e709-4a33-aa63-42d811ad02b2" />
Dashboard: <img width="2076" height="1274" alt="Screenshot 2026-06-09 001900" src="https://github.com/user-attachments/assets/638d324d-ce23-435e-9226-44b51c3c554c" />

---

## Authentication Flow

### 1. **Registration**
```
User fills form (username, password)
  ↓
Backend validates input
  ↓
Password hashed using Werkzeug (never store plaintext)
  ↓
User inserted into SQLite database
  ↓
Redirect to login
```

### 2. **Login**
```
User enters username + password
  ↓
Query database for username
  ↓
If found → compare submitted password with hashed password
  ↓
If match → create session['user'] = username
  ↓
Redirect to dashboard
  ↓
If no match → show error, stay on login
```

### 3. **Protected Route (Dashboard)**
```
User requests /dashboard
  ↓
Check if 'user' exists in session
  ↓
If yes → show dashboard, welcome message
  ↓
If no → redirect to /login
```

### 4. **Logout**
```
User clicks logout
  ↓
Clear session['user']
  ↓
Destroy session
  ↓
Redirect to /login
```

---

## Routes

| Route | Method | Purpose | Protected |
|-------|--------|---------|-----------|
| `/register` | GET, POST | User signup form + create account | No |
| `/login` | GET, POST | User login form + authenticate | No |
| `/dashboard` | GET | Show user profile | **Yes** |
| `/logout` | GET | Clear session, logout | **Yes** |

---

## Security Concepts

### Password Hashing
- Never store passwords as plaintext
- Use `werkzeug.security.generate_password_hash()` to hash
- Use `werkzeug.security.check_password_hash()` to verify
- Hash = one-way function (cannot reverse)

**Why:** If database is breached, passwords remain safe.

### Sessions
- Store user info in `session` object (Flask)
- Session data stored server-side
- Client gets session cookie (secure token)
- Check `session['user']` to verify logged-in user

**Why:** User doesn't send password every request. Session proves identity.

### Protected Routes
- Decorator or check at route start
- If `'user' not in session` → redirect to login
- Prevents unauthorized access

**Why:** Only authenticated users access private data.

### Logout
- Clear session with `session.pop('user', None)`
- Destroy session on server
- Redirect to login

**Why:** Prevents account hijacking if device is shared.

---

## Database Schema

### users table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
```

- `id`: Unique identifier
- `username`: Must be unique (no duplicates)
- `password`: Hashed password (never plaintext)

---

## Setup & Run

### Install Dependencies
```bash
pip install flask werkzeug
```

### Run App
```bash
python app.py
```

### Access
```
http://127.0.0.1:5000/register
```

---

## File Structure
```
python-fullstack-task2/
├── app.py                 # Flask routes + authentication logic
├── database.db            # SQLite database (auto-created)
├── templates/
│   ├── register.html      # Registration form
│   ├── login.html         # Login form
│   └── dashboard.html     # Protected user dashboard
└── static/
    └── style.css          # Styling
```

---

## Key Code Snippets

### Hash Password on Register
```python
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash(password)
db.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
           (username, password_hash))
```

### Verify Password on Login
```python
from werkzeug.security import check_password_hash

user = db.execute("SELECT * FROM users WHERE username = ?", 
                  (username,)).fetchone()
if user and check_password_hash(user['password'], password):
    session['user'] = username
    return redirect('/dashboard')
```

### Protect Route
```python
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])
```

### Logout
```python
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')
```

---

## Security Best Practices (What You Learn)

✅ Hash passwords (never plaintext)  
✅ Use sessions for user identity  
✅ Protect routes with authentication check  
✅ Clear session on logout  
✅ Validate user input  
✅ Use HTTPS in production (not localhost)  
✅ Set secure secret key (not "secure-secret-key")  

---

## Interview Questions (Mandatory)

1. **Why hash passwords?** → One-way function. Hacker cannot reverse.
2. **What is session?** → Server-side storage linked to user via cookie.
3. **How do you protect routes?** → Check if `'user'` in `session` before rendering.
4. **What happens on logout?** → `session.pop('user')` clears identity.
5. **Difference between password hash and encryption?** → Hash = one-way, Encryption = reversible with key.

---

## Next Steps

- Add email verification
- Implement password reset
- Add role-based access control (admin, user)
- Use database ORM (SQLAlchemy)
- Deploy to production (Heroku, AWS)
- Add CSRF protection
- Implement rate limiting (prevent brute-force)

---

**Built for:** Maincrafts Technology - Python Full Stack Development  
**Task:** Task 2 - User Authentication System
