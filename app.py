from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_todos():
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM todos ORDER BY created_at DESC')
    todos = c.fetchall()
    conn.close()
    return todos

@app.route('/')
def index():
    todos = get_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    description = request.form.get('description', '')
    
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('INSERT INTO todos (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('UPDATE todos SET completed = 1 WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)