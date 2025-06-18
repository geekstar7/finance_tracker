from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, description TEXT, amount REAL, type TEXT, category TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()

    income = sum(t[2] for t in transactions if t[3] == 'income')
    expense = sum(t[2] for t in transactions if t[3] == 'expense')
    balance = income - expense

    return render_template('index.html', transactions=transactions,
                           income=income, expense=expense, balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = float(request.form['amount'])
    type_ = request.form['type']
    category = request.form['category']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (description, amount, type, category) VALUES (?, ?, ?, ?)",
              (description, amount, type_, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/data')
def data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    results = c.fetchall()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    import os
app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

