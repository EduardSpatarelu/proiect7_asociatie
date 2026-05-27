import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db_connection

class Payment:
    """
    Reprezinta o plata efectuata de un locatar.
    Corespunde entitatii 'Payment' din diagrama de clase si ER diagram.
    """

    def __init__(self, id: int, amount: float, date: str, apartment_id: int):
        self.id = id
        self.amount = amount
        self.date = date
        self.apartment_id = apartment_id

    @staticmethod
    def get_all() -> list:
        """
        Returneaza toate platile inregistrate.
        Fiecare element: (id, apartment_id, amount, date)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, apartment_id, amount, date "
                "FROM payments ORDER BY date DESC;"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print("Eroare la preluare plati:", e)
            return []

    @staticmethod
    def get_by_apartment(apartment_id: int) -> list:
        """Returneaza platile unui apartament specific."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, apartment_id, amount, date "
                "FROM payments WHERE apartment_id = %s ORDER BY date DESC;",
                (apartment_id,)
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print("Eroare la preluare plati apartament:", e)
            return []

    @staticmethod
    def adauga(apartment_id: int, amount: float, date: str) -> bool:
        """
        Inregistreaza o plata noua si actualizeaza datoria apartamentului.
        Corespunde secventei din Sequence Diagram:
          INSERT INTO payments -> UPDATE Apartments SET Debt = Debt - Amount
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # INSERT INTO Payments
            cursor.execute(
                "INSERT INTO payments (apartment_id, amount, date) VALUES (%s, %s, %s)",
                (apartment_id, amount, date)
            )

            # UPDATE Apartment SET Debt = Debt - Amount (daca exista coloana current_debt)
            try:
                cursor.execute(
                    "UPDATE Apartments SET current_debt = current_debt - %s "
                    "WHERE id = %s",
                    (amount, apartment_id)
                )
            except Exception:
                pass  # Coloana current_debt poate sa nu existe in toate versiunile

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Eroare la adaugare plata:", e)
            return False
