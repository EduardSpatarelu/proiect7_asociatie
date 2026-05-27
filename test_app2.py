import pytest
from app2 import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_key'
    with app.test_client() as client:
        yield client

# python -m pytest test_app2.py -v

# TESTE DE AUTENTIFICARE (3)

def test_login_page_loads(client):
    """1. Verifică dacă pagina de login se încarcă corect."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Autentificare" in response.data


def test_dashboard_redirect_if_not_logged_in(client):
    """2. Verifică dacă userul e trimis la login dacă nu e logat."""
    response = client.get('/', follow_redirects=True)
    assert "login" in response.request.path.lower()


def test_logout_clears_session(client):
    """3. Verifică dacă logout-ul funcționează."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    client.get('/logout')
    with client.session_transaction() as sess_dupa:
        assert 'user_id' not in sess_dupa


# TESTE DE NAVIGARE ȘI RUTE (6)

@patch('models.apartment.get_db_connection')
def test_dashboard_access_authorized(mock_db, client):
    """4. Verifică accesul la dashboard pentru un user logat."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_db.return_value.cursor.return_value.fetchall.return_value = []
    response = client.get('/')
    assert response.status_code == 200


@patch('models.supplier.get_db_connection')
def test_facturi_page_loads(mock_db, client):
    """5. Verifică încărcarea paginii de facturi."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_db.return_value.cursor.return_value.fetchall.return_value = []
    response = client.get('/facturi')
    assert response.status_code == 200


@patch('models.apartment.get_db_connection')
def test_apa_page_loads(mock_db, client):
    """6. Verifică încărcarea paginii de consum apă."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_db.return_value.cursor.return_value.fetchall.return_value = []
    mock_db.return_value.cursor.return_value.fetchone.return_value = [0]
    response = client.get('/apa')
    assert response.status_code == 200


@patch('models.apartment.get_db_connection')
@patch('models.payment.get_db_connection')
def test_plati_page_loads(mock_payment_db, mock_apt_db, client):
    """7. Verifică încărcarea paginii de plăți."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_payment_db.return_value.cursor.return_value.fetchall.return_value = []
    mock_apt_db.return_value.cursor.return_value.fetchall.return_value = []
    response = client.get('/plati')
    assert response.status_code == 200


@patch('models.financial_manager.get_db_connection')
def test_rapoarte_page_loads(mock_db, client):
    """8. Verifică încărcarea paginii de rapoarte."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    mock_cursor = MagicMock()
    mock_db.return_value.cursor.return_value = mock_cursor
    # Simuleaza: nr_facturi=1, nr_apa=1, total_inv, total_sal, total_rooms, apartamente
    mock_cursor.fetchone.side_effect = [(1,), (1,), (1000.0,), (500.0,), (10,)]
    mock_cursor.fetchall.return_value = [(1, 3, 2)]
    response = client.get('/rapoarte')
    assert response.status_code == 200


def test_404_on_invalid_route(client):
    """9. Verifică dacă rutele inexistente dau 404."""
    response = client.get('/pagina_care_nu_exista')
    assert response.status_code == 404


# TESTE FUNCȚIONALE / LOGICĂ BAZĂ DE DATE (6)

@patch('models.apartment.get_db_connection')
def test_add_apartment_post(mock_db, client):
    """10. Verifică ruta de adăugare apartament (POST)."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    response = client.post('/add_apartment', data={
        'room_count': 3,
        'resident_count': 2
    })
    assert response.status_code == 302


@patch('models.apartment.get_db_connection')
def test_add_water_post(mock_db, client):
    """11. Verifică ruta de adăugare consum apă (POST)."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    response = client.post('/add_water', data={
        'apartament_id': 1,
        'index_value': 150,
        'date': '2026-05-15'
    })
    assert response.status_code == 302


@patch('models.payment.get_db_connection')
def test_add_payment_post(mock_db, client):
    """12. Verifică ruta de adăugare plată (POST)."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    response = client.post('/add_payment', data={
        'apartment_id': 1,
        'amount': 200.50,
        'date': '2026-05-15'
    })
    assert response.status_code == 302


def test_maintenance_calculation_logic(client):
    """13. Testează logica matematică a formulei de calcul întreținere."""
    # Formula: ((TotalFacturi + TotalSalarii) / TotalCamere) * CamereApt * (Locatari * 0.5)
    from models.financial_manager import FinancialManager
    fm = FinancialManager()
    rezultat = fm.calculate_monthly_fee(
        apartment_id=1,
        room_count=2,
        resident_count=2,
        total_invoices=1000,
        total_salaries=1000,
        total_rooms=10
    )
    # ((1000 + 1000) / 10) * 2 * (2 * 0.5) = 200 * 2 * 1 = 400
    assert rezultat == 400.0


@patch('models.user.get_db_connection')
def test_login_invalid_credentials(mock_db, client):
    """14. Verifică login cu date greșite."""
    mock_db.return_value.cursor.return_value.fetchone.return_value = None
    response = client.post('/login', data={'username': 'wrong', 'password': 'wrong'})
    assert b"parola" in response.data.lower() or response.status_code == 200


@patch('models.apartment.get_db_connection')
def test_db_connection_fail_handling(mock_db, client):
    """15. Verifică comportamentul la eroare de conexiune DB (pagina /apa)."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
    # Simulam eroare DB — get_db_connection arunca exceptie
    mock_db.side_effect = Exception("DB Down")
    response = client.get('/apa')
    # Pagina trebuie sa se incarce chiar si fara DB (lista goala)
    assert response.status_code == 200
