from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
# Această cheie permite Flask să cripteze datele de login
app.secret_key = 'cheie_secreta_bloc_x69'

def get_db_connection():
    conn = psycopg2.connect(
        dbname="asociatie_db",
        user="postgres",
        password="1133",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, role FROM users WHERE username = %s AND password_hash = %s", (u, p))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'], session['username'], session['role'] = user[0], user[1], user[2]
            return redirect(url_for('dashboard'))
        error = "Utilizator sau parolă greșită!"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def dashboard():
    # DACĂ NU EȘTI LOGAT, TE TRIMITE LA LOGIN
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_count, resident_count FROM Apartments ORDER BY id;")
    apartamente = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('index.html', apartamente=apartamente)

@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    # Preluăm datele din formularul HTML pentru apartamente
    room_count = request.form.get('room_count')
    resident_count = request.form.get('resident_count')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Inserăm noul apartament
    cursor.execute(
        "INSERT INTO Apartments (room_count, resident_count) VALUES (%s, %s)",
        (room_count, resident_count)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('dashboard'))

@app.route('/facturi')
def facturi():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Extragem facturile existente și numele furnizorului
    cursor.execute("""
        SELECT i.id, s.name, i.amount, i.date 
        FROM Invoices i 
        JOIN Suppliers s ON i.supplier_id = s.id 
        ORDER BY i.date DESC;
    """)
    facturi_lista = cursor.fetchall()
    
    # Extragem furnizorii pentru meniul derulant (dropdown) din formular
    cursor.execute("SELECT id, name FROM Suppliers;")
    furnizori = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('facturi.html', facturi=facturi_lista, furnizori=furnizori)

@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    supplier_id = request.form.get('supplier_id')
    amount = request.form.get('amount')
    date = request.form.get('date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Inserăm factura conform cerinței REQ-33
    cursor.execute(
        "INSERT INTO Invoices (amount, date, supplier_id) VALUES (%s, %s, %s)",
        (amount, date, supplier_id)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('facturi'))

@app.route('/rapoarte')
def rapoarte():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Preluăm totalurile necesare pentru formula REQ-41
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM Invoices;")
    total_invoices = float(cursor.fetchone()[0])
    
    cursor.execute("SELECT COALESCE(SUM(salariu_brut), 0) FROM Employees;")
    total_salaries = float(cursor.fetchone()[0])
    
    cursor.execute("SELECT COALESCE(SUM(room_count), 0) FROM Apartments;")
    total_rooms = int(cursor.fetchone()[0])
    
    # Preluăm apartamentele pentru a aplica formula
    cursor.execute("SELECT id, room_count, resident_count FROM Apartments ORDER BY id;")
    apartamente = cursor.fetchall()
    
    raport_final = []
    
    # Aplicăm formula pentru fiecare apartament în parte
    if total_rooms > 0:
        for apt in apartamente:
            apt_id, apart_rooms, residents = apt
            suma = ((total_invoices + total_salaries) / total_rooms) * apart_rooms * (residents * 0.5)
            
            raport_final.append({
                'id': apt_id,
                'camere': apart_rooms,
                'locatari': residents,
                'suma_plata': round(suma, 2)
            })
            
    cursor.close()
    conn.close()
    
    return render_template('rapoarte.html', 
                           raport=raport_final, 
                           total_invoices=total_invoices, 
                           total_salaries=total_salaries)

@app.route('/apa')
def apa():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, apartament_id, index_value, date 
            FROM waterconsumption 
            ORDER BY date DESC;
        """)
        consumuri = cursor.fetchall()
    except Exception as e:
        print("Eroare la extragerea datelor:", e)
        consumuri = []
        conn.rollback()
    
    cursor.execute("SELECT id FROM Apartments ORDER BY id;")
    apartamente = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('apa.html', consumuri=consumuri, apartamente=apartamente)

@app.route('/add_water', methods=['POST'])
def add_water():
    apartament_id = request.form.get('apartament_id')
    index_value = request.form.get('index_value')
    date = request.form.get('date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO waterconsumption (apartament_id, index_value, date) VALUES (%s, %s, %s)",
        (apartament_id, index_value, date)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('apa'))

@app.route('/plati')
def plati():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, apartment_id, amount, date 
            FROM payments 
            ORDER BY date DESC;
        """)
        plati_lista = cursor.fetchall()
    except Exception as e:
        print("Eroare la extragerea plăților:", e)
        plati_lista = []
        conn.rollback()
    
    cursor.execute("SELECT id FROM Apartments ORDER BY id;")
    apartamente = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('plati.html', plati=plati_lista, apartamente=apartamente)

@app.route('/add_payment', methods=['POST'])
def add_payment():
    # Preluăm datele din formular folosind noul nume
    apartment_id = request.form.get('apartment_id')
    amount = request.form.get('amount')
    date = request.form.get('date')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Inserăm în coloanele tale specifice
    cursor.execute(
        "INSERT INTO payments (apartment_id, amount, date) VALUES (%s, %s, %s)",
        (apartment_id, amount, date)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('plati'))

if __name__ == '__main__':
    app.run(debug=True)