import sqlite3
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SECURITY WARNING: Always set a strong, unpredictable secret key. 
# In a production environment, load this from an environment variable.
app.secret_key = 'super_secret_session_key_change_in_production'

DATABASE = 'database.db'

# --- DATABASE MANAGEMENT ---

def get_db():
    """
    SECURITY BEST PRACTICE: Establishes a database connection for each request thread.
    Using g ensures the database cursor is clean and isolated per web request.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Use Row factory to allow accessing columns by key names
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """
    Closes the database connection at the end of each request lifecycle.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """
    Runs on startup to initialize the SQLite schema.
    """
    with app.app_context():
        db = get_db()
        # SECURITY: Auto-increment primary key keeps user IDs unique and incremental.
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        db.commit()

# --- INPUT FORM VALIDATION ---

def validate_username(username):
    """
    Validates username format and length.
    """
    if not username or not username.strip():
        return "Username is required."
    
    if len(username) < 3 or len(username) > 30:
        return "Username must be between 3 and 30 characters."
        
    # SECURITY: Restricting username characters to alphanumeric and underscores
    # prevents issues with encoding, path traversal, or script injection.
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return "Username can only contain alphanumeric characters and underscores."
        
    return None

def validate_password(password):
    """
    Validates password complexity.
    """
    if not password:
        return "Password is required."
        
    if len(password) < 8:
        return "Password must be at least 8 characters long."
        
    # SECURITY: Require digits, uppercase, and lowercase characters for password strength.
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit (0-9)."
        
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter (A-Z)."
        
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter (a-z)."
        
    return None

# --- WEB APPLICATION ROUTES ---

@app.route('/')
def index():
    """
    Root route redirects depending on session state.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register Route (GET / POST)
    Handles creation of new user records.
    """
    # SECURITY: If user is logged in, redirect them away from register form.
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        errors = {}
        
        # Run validations
        username_err = validate_username(username)
        if username_err:
            errors['username'] = username_err
            
        password_err = validate_password(password)
        if password_err:
            errors['password'] = password_err
            
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
            
        if not errors:
            db = get_db()
            
            # SECURITY: Using parameterized queries (?) strictly prevents SQL Injection attacks.
            cursor = db.execute('SELECT id FROM users WHERE username = ?', (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                errors['username'] = "Username is already taken."
            else:
                try:
                    # SECURITY: werkzeug.security.generate_password_hash uses PBKDF2/scrypt 
                    # with a random salt to prevent brute force and rainbow table cracking.
                    # Plaintext passwords are NEVER stored in the database.
                    hashed_pwd = generate_password_hash(password)
                    
                    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pwd))
                    db.commit()
                    
                    flash("Account successfully created! Please sign in.", "success")
                    return redirect(url_for('login'))
                except sqlite3.Error as e:
                    flash(f"A database error occurred: {str(e)}", "error")
                    
        return render_template('register.html', errors=errors, values={'username': username})
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login Route (GET / POST)
    Validates user credentials and initiates the session.
    """
    # SECURITY: If user is logged in, redirect them away from login form.
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        errors = {}
        
        if not username:
            errors['username'] = "Username is required."
        if not password:
            errors['password'] = "Password is required."
            
        if not errors:
            db = get_db()
            # SECURITY: Parameterized query to avoid SQL Injection.
            cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            # SECURITY: Using constant-time check_password_hash checks the hashed password
            # and prevents timing side-channel analysis.
            if user and check_password_hash(user['password'], password):
                # Session initialization
                session['user_id'] = user['id']
                session['username'] = user['username']
                
                # Check for "Remember me" option
                if remember:
                    session.permanent = True  # Extends session cookie to 31 days
                else:
                    session.permanent = False
                    
                flash(f"Welcome back, {username}!", "success")
                return redirect(url_for('dashboard'))
            else:
                # SECURITY BEST PRACTICE: Generic warning prevents user enumeration.
                # It does not disclose whether the username or password was wrong.
                flash("Invalid username or password.", "error")
                errors['username'] = "Invalid credentials"
                errors['password'] = "Invalid credentials"
                
        return render_template('login.html', errors=errors, values={'username': username, 'remember': remember})
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """
    Dashboard Route (GET)
    Protected home route displaying session statistics.
    """
    # SECURITY: Session checks ensure that unauthorized users cannot bypass auth filters.
    if 'user_id' not in session:
        flash("Access Denied: Please sign in to view the dashboard.", "error")
        return redirect(url_for('login'))
        
    return render_template('dashboard.html', user_id=session['user_id'], username=session['username'])

@app.route('/logout')
def logout():
    """
    Logout Route (GET)
    Clears the session cookie.
    """
    # SECURITY: session.clear() fully destroys the session dict client and server side.
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Setup SQLite tables on startup
    init_db()
    # Run dev server locally on localhost:5000
    app.run(debug=True, port=5000)
