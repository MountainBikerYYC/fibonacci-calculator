from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'fibonacci.db'

# Create empty database
def create_tables():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS fibonacci (n INTEGER PRIMARY KEY, result TEXT)")

# Calculation
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    # Check in database if already computed
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT result FROM fibonacci WHERE n=?", (n,))
        result = cursor.fetchone()
        # if yes, return that entire result array
        if result:
            fib_str = result[0]
            return result[0]

        fib = [0, 1]
        # compute the numbers
        while len(fib) < n:
            fib.append(fib[-1] + fib[-2])

        # Convert and seperate using commas
        fib_result = ', '.join(map(str, fib))

        # Save the resulting array to the database
        cursor.execute("INSERT OR REPLACE INTO fibonacci (n, result) VALUES (?, ?)", (n, fib_result))
        db.commit()

        return fib

# Initialize database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        create_tables()
    return db

# Close database
def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))

        return redirect(f'/fibonacci/{n}')

    return render_template('index.html')

# results page
@app.route('/fibonacci/<int:n>')
def fibonacci_results(n):

    fib_result = fibonacci(n)
    return render_template('fibonacci_results.html', n=n, fib_result=fib_result)

if __name__ == '__main__':
    app.teardown_appcontext(close_db)
    app.run(debug=True)
