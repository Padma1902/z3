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
@app.route('/edit_animal/<int:id>', methods=['GET', 'POST'])
def edit_animal(id):
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        gender = request.form['gender']
        caretaker = request.form['caretaker']
        cage = request.form['cage']

        c.execute('''
            UPDATE animals 
            SET name = ?, species = ?, gender = ?, caretaker = ?, cage = ? 
            WHERE id = ?
        ''', (name, species, gender, caretaker, cage, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_animals'))  # replace with your actual view route name

    c.execute('SELECT * FROM animals WHERE id = ?', (id,))
    animal = c.fetchone()
    conn.close()
    return render_template('edit_animal.html', animal=animal)
@app.route('/edit_booking/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    conn = sqlite3.connect('zoo.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        visitor = request.form['visitor']
        booking_type = request.form['type']
        price = request.form['price']

        cursor.execute("""
            UPDATE bookings
            SET visitor = ?, type = ?, price = ?
            WHERE id = ?
        """, (visitor, booking_type, price, booking_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_bookings'))

    else:  # GET request
        cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        record = cursor.fetchone()
        conn.close()
        return render_template('edit_booking.html', record=record)
@app.route('/edit_caretaker/<int:id>', methods=['GET'])
def edit_caretaker(id):
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM caretakers WHERE id=?", (id,))
    caretaker = c.fetchone()
    conn.close()
    return render_template('edit_caretaker.html', caretaker=caretaker)
@app.route('/edit_vet/<int:id>', methods=['GET', 'POST'])
def edit_vet(id):
    conn = sqlite3.connect('zoo.db')
    c = conn.cursor()

    if request.method == 'POST':
        doctor = request.form['doctor']
        phone = request.form['phone']
        checkup_time = request.form['checkup_time']
        c.execute("UPDATE vet_checkups SET doctor = ?, phone = ?, checkup_time = ? WHERE id = ?", 
                  (doctor, phone, checkup_time, id))
        conn.commit()
        conn.close()
        return redirect('/view_vet')  # your vet checkups view page

    c.execute("SELECT * FROM vet_checkups WHERE id = ?", (id,))
    record = c.fetchone()
    conn.close()
    return render_template('edit_vet.html', record=record)





if __name__ == '__main__':
    init_db()
    app.run(debug=True)
