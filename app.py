from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS animals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, species TEXT, gender TEXT,
                    caretaker TEXT, cage_number TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS caretakers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, caretaker_id TEXT, cage_number TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vet_checkups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    doctor_name TEXT, phone TEXT, checkup_time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visitor_name TEXT, visitor_type TEXT, price INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        conn = sqlite3.connect('zoo.db')
        c = conn.cursor()
        username = request.form['username']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            return redirect('/animal')
        else:
            msg = 'Invalid login'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['POST'])
def register():
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (request.form['username'], request.form['password']))
        conn.commit()
    except:
        return "User already exists!"
    return redirect('/login')

@app.route('/animal', methods=['GET', 'POST'])
def animal():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['species'],
            request.form['gender'],
            request.form['caretaker'],
            request.form['cage']
        )
        conn = sqlite3.connect('zoo.db')
        c = conn.cursor()
        c.execute("INSERT INTO animals (name, species, gender, caretaker, cage_number) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect('/caretaker')
    return render_template('animal.html')

@app.route('/caretaker', methods=['GET', 'POST'])
def caretaker():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['caretaker_id'],
            request.form['cage']
        )
        conn = sqlite3.connect('zoo.db')
        c = conn.cursor()
        c.execute("INSERT INTO caretakers (name, caretaker_id, cage_number) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect('/vet')
    return render_template('caretaker.html')

@app.route('/vet', methods=['GET', 'POST'])
def vet():
    if request.method == 'POST':
        data = (
            request.form['doctor'],
            request.form['phone'],
            request.form['checkup_time']
        )
        conn = sqlite3.connect('zoo.db')
        c = conn.cursor()
        c.execute("INSERT INTO vet_checkups (doctor_name, phone, checkup_time) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()
        return redirect('/booking')
    return render_template('vet.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        data = (
            request.form['visitor'],
            request.form['type'],
            request.form['price']
        )
        conn = sqlite3.connect('zoo.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (visitor_name, visitor_type, price) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()
    return render_template('booking.html')
@app.route('/view_animals')
def view_animals():
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM animals")
    rows = c.fetchall()
    conn.close()
    return render_template('view_animals.html', records=rows)

@app.route('/view_caretakers')
def view_caretakers():
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM caretakers")
    rows = c.fetchall()
    conn.close()
    return render_template('view_caretakers.html', records=rows)

@app.route('/view_vet')
def view_vet():
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vet_checkups")
    rows = c.fetchall()
    conn.close()
    return render_template('view_vet.html', records=rows)

@app.route('/view_bookings')
def view_bookings():
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    rows = c.fetchall()
    conn.close()
    return render_template('view_bookings.html', records=rows)

@app.route('/delete_animal/<int:animal_id>', methods=['POST'])
def delete_animal(animal_id):
    conn = sqlite3.connect('zoo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM animals WHERE id = ?", (animal_id,))
    conn.commit()
    conn.close()
    return redirect('/view_animals')
@app.route('/delete_caretaker/<int:caretaker_id>', methods=['POST'])
def delete_caretaker(caretaker_id):
    conn = sqlite3.connect('zoo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM caretakers WHERE id = ?", (caretaker_id,))
    conn.commit()
    conn.close()
    return redirect('/view_caretakers')
@app.route('/delete_vet/<int:vet_id>', methods=['POST'])
def delete_vet(vet_id):
    conn = sqlite3.connect('zoo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vet_checkups WHERE id = ?", (vet_id,))
    conn.commit()
    conn.close()
    return redirect('/view_vets')
@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    conn = sqlite3.connect('zoo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect('/view_bookings')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
