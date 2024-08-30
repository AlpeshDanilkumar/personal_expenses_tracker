from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('finance_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

@app.route('/add_transaction', methods=('GET', 'POST'))
def add_transaction():
    if request.method == 'POST':
        type = request.form['type']
        amount = request.form['amount']
        category = request.form['category']
        date = datetime.now().isoformat()

        conn = get_db_connection()
        conn.execute('INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)',
                     (type, amount, category, date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_transaction.html')

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

