from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)

## to complete
app.config['SECRET_KEY'] = 'your_secret_key_here'  
app.config['DATABASE'] = 'fibonacci.db' 

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib = [0, 1]
    while len(fib) < n:
        fib.append(fib[-1] + fib[-2])
    return fib

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))
        fib_numbers = fibonacci(n)
        fib_str = ', '.join(map(str, fib_numbers))

        # save result to sqlite3 database, to change to serverless
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT OR REPLACE INTO fibonacci (n, result) VALUES (?, ?)", (n, fib_str))
            db.commit()

        return redirect(f'/fibonacci/{n}')

    return render_template('index.html')

@app.route('/fibonacci/<int:n>')
def show_fibonacci_numbers(n):
    # Retrieve the Fibonacci numbers from the database
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT result FROM fibonacci WHERE n=?", (n,))
        result = cursor.fetchone()
        fib_str = result[0] if result else None

    return render_template('fibonacci_numbers.html', n=n, fib_str=fib_str)

if __name__ == '__main__':
    app.teardown_appcontext(close_db)
    app.run(debug=True)
