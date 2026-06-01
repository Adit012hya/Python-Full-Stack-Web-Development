from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__)

# Ensure DB is initialized at import/startup (Flask 3 removed before_first_request)
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if name and email:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            conn.commit()
            conn.close()
        return redirect('/?msg=added')

    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)


@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/?msg=deleted')

if __name__ == '__main__':
    app.run(debug=True)
