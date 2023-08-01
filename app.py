from flask import Flask, render_template, request, redirect, g
import sqlite3
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['DATABASE'] = 'fibonacci.db'

def create_tables():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS fibonacci (n INTEGER PRIMARY KEY, result TEXT)")

def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT result FROM fibonacci WHERE n=?", (n,))
        result = cursor.fetchone()
        if result:
            # If result exists in the database, retrieve it and return
            fib_str = result[0]
            return result[0]

        # If result doesn't exist in the database, compute the Fibonacci numbers and store them in the database
        fib = [0, 1]
        while len(fib) < n:
            fib.append(fib[-1] + fib[-2])

        # Convert the list of Fibonacci numbers to a comma-separated string
        fib_str = ', '.join(map(str, fib))

        # Save the computed result to the database
        cursor.execute("INSERT OR REPLACE INTO fibonacci (n, result) VALUES (?, ?)", (n, fib_str))
        db.commit()

        return fib

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        create_tables()
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Rest of your code remains the same...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))
        fib_numbers = fibonacci(n)

        return redirect(f'/fibonacci/{n}')

    return render_template('index.html')

@app.route('/fibonacci/<int:n>')
def show_fibonacci_numbers(n):
    # Retrieve the Fibonacci numbers from the database

    # start_time = time.time()
    fib_result = fibonacci(n)
    # end_time = time.time()
    # print(f"Time taken to compute Fibonacci({n}): {end_time - start_time:.6f} seconds")

    return render_template('fibonacci_numbers.html', n=n, fib_result=fib_result)

if __name__ == '__main__':
    app.teardown_appcontext(close_db)
    app.run(debug=True)
