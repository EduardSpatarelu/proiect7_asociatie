from flask import Flask, render_template, request, redirect, url_for, session

from models.user import User
from models.apartment import Apartment, WaterConsumption
from models.supplier import Supplier, Invoice
from models.payment import Payment
from models.financial_manager import FinancialManager

app = Flask(__name__)
app.secret_key = 'cheie_secreta_bloc_x69'

# Autentificare

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        try:
            user_obj = User(None, u, p, None, None)
            user_data = user_obj.login(u, p)
            if user_data:
                session['user_id'] = user_data['id']
                session['username'] = user_data['username']
                session['role'] = user_data['role']
                return redirect(url_for('dashboard'))
            error = "Utilizator sau parola gresita."
        except Exception:
            error = "Eroare de conexiune la serverul de baza de date."
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Dashboard — Manage Apartment/Resident Info

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    apartamente = Apartment.get_all()
    # Convertim obiectele la tuple pentru compatibilitate cu template-ul existent
    apartamente_tuples = [(a.id, a.room_count, a.resident_count) for a in apartamente]
    return render_template('index.html', apartamente=apartamente_tuples)


@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    room_count = request.form.get('room_count')
    resident_count = request.form.get('resident_count')
    Apartment.adauga(int(room_count), int(resident_count))
    return redirect(url_for('dashboard'))


# Facturi — Manage Supplier Contracts + Add Monthly Invoices

@app.route('/facturi')
def facturi():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    facturi_lista = Invoice.get_all()
    furnizori = Supplier.get_all()
    return render_template('facturi.html', facturi=facturi_lista, furnizori=furnizori)


@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    supplier_id = int(request.form.get('supplier_id'))
    amount = float(request.form.get('amount'))
    date = request.form.get('date')
    Invoice.adauga(supplier_id, amount, date)
    return redirect(url_for('facturi'))


# Rapoarte — Generate Monthly Financial Reports

@app.route('/rapoarte')
def rapoarte():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    fm = FinancialManager()
    result = fm.generate_report()
    return render_template(
        'rapoarte.html',
        raport=result.get('raport', []),
        total_invoices=result.get('total_invoices', 0.0),
        total_salaries=result.get('total_salaries', 0.0)
    )


# Apa — Record Water Consumption

@app.route('/apa')
def apa():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    consumuri = WaterConsumption.get_all()
    apartamente = Apartment.get_ids()
    return render_template('apa.html', consumuri=consumuri, apartamente=apartamente)


@app.route('/add_water', methods=['POST'])
def add_water():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    apartament_id = int(request.form.get('apartament_id'))
    index_value = int(request.form.get('index_value'))
    date = request.form.get('date')
    WaterConsumption.adauga(apartament_id, index_value, date)
    return redirect(url_for('apa'))


# Plati — Log Resident Payments

@app.route('/plati')
def plati():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    plati_lista = Payment.get_all()
    apartamente = Apartment.get_ids()
    return render_template('plati.html', plati=plati_lista, apartamente=apartamente)


@app.route('/add_payment', methods=['POST'])
def add_payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    apartment_id = int(request.form.get('apartment_id'))
    amount = float(request.form.get('amount'))
    date = request.form.get('date')
    Payment.adauga(apartment_id, amount, date)
    return redirect(url_for('plati'))


if __name__ == '__main__':
    app.run(debug=True)
