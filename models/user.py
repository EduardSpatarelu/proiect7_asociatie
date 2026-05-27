from proiect7_asociatie.database import get_db_connection


class User:
    """
    Clasa de baza pentru utilizatorii sistemului.
    Corespunde entitatii 'User' din diagrama de clase.
    """

    def __init__(self, id: int, username: str, password_hash: str,
                 email: str, telefon: str):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.telefon = telefon

    def login(self, username: str, password: str):
        """
        Verifica credentialele in baza de date.
        Returneaza un dict cu datele userului daca reuseste, altfel None.
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, role FROM users "
                "WHERE username = %s AND password_hash = %s",
                (username, password)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                return {"id": user[0], "username": user[1], "role": user[2]}
            return None
        except Exception as e:
            print("Eroare la autentificare:", e)
            raise

    def logout(self):
        """Sterge sesiunea curenta (gestionata de Flask in app.py)."""
        pass  # logica de sesiune ramane in Flask

    def reset_password(self, user_id: int, new_password: str) -> bool:
        """Reseteaza parola unui utilizator dupa ID."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (new_password, user_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Eroare la resetare parola:", e)
            return False

    @staticmethod
    def get_all_users():
        """Returneaza toti utilizatorii din sistem."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users ORDER BY id;")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return users
        except Exception as e:
            print("Eroare la preluare utilizatori:", e)
            return []


class Administrator(User):
    """
    Subclasa User cu drepturi extinse de administrare.
    Corespunde entitatii 'Administrator' din diagrama de clase.
    """

    def __init__(self, id: int, username: str, password_hash: str,
                 email: str, telefon: str, numar_atestat: str):
        super().__init__(id, username, password_hash, email, telefon)
        self.numar_atestat = numar_atestat

    def genereaza_raport_lunar(self) -> dict:
        """
        Declanseaza generarea raportului lunar.
        Delega calculul catre FinancialManager.
        Returneaza datele raportului sau un dict gol la eroare.
        """
        from proiect7_asociatie.models.financial_manager import FinancialManager
        fm = FinancialManager()
        return fm.generate_report()

    def calculeaza_intretinere(self, apartment_id: int) -> float:
        """Calculeaza cota de intretinere pentru un apartament specific."""
        from proiect7_asociatie.models.financial_manager import FinancialManager
        fm = FinancialManager()
        report = fm.generate_report()
        for entry in report.get("raport", []):
            if entry["id"] == apartment_id:
                return entry["suma_plata"]
        return 0.0

    def adauga_factura(self, furnizor_id: int, suma: float, data: str) -> bool:
        """Adauga o factura noua in sistem."""
        from proiect7_asociatie.models.supplier import Invoice
        return Invoice.adauga(furnizor_id, suma, data)

    def inregistreaza_plata(self, apartment_id: int, suma: float, data: str) -> bool:
        """Inregistreaza o plata efectuata de un locatar."""
        from proiect7_asociatie.models.payment import Payment
        return Payment.adauga(apartment_id, suma, data)

    def gestioneaza_contracte(self):
        """Returneaza lista contractelor/furnizorilor activi."""
        from proiect7_asociatie.models.supplier import Supplier
        return Supplier.get_all()

    def notifica_restantieri(self) -> list:
        """
        Returneaza lista apartamentelor cu datorii restante.
        (Placeholder - logica extinsa poate fi adaugata ulterior)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM Apartments WHERE current_debt > 0 ORDER BY id;"
            )
            restantieri = cursor.fetchall()
            cursor.close()
            conn.close()
            return [r[0] for r in restantieri]
        except Exception as e:
            print("Eroare la preluare restantieri:", e)
            return []
