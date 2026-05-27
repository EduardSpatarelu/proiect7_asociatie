from proiect7_asociatie.database import get_db_connection


class Supplier:
    """
    Reprezinta un furnizor de servicii al asociatiei.
    Corespunde entitatii 'Supplier' din diagrama de clase si ER diagram.
    """

    def __init__(self, id: int, name: str, fiscal_code: str,
                 contract_details: str = ""):
        self.id = id
        self.name = name
        self.fiscal_code = fiscal_code
        self.contract_details = contract_details

    @staticmethod
    def get_all() -> list:
        """Returneaza toti furnizorii inregistrati."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM Suppliers;")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print("Eroare la preluare furnizori:", e)
            return []

    @staticmethod
    def adauga(name: str, fiscal_code: str) -> bool:
        """Adauga un furnizor nou."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Suppliers (name, fiscal_code) VALUES (%s, %s)",
                (name, fiscal_code)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Eroare la adaugare furnizor:", e)
            return False


class Invoice:
    """
    Reprezinta o factura emisa de un furnizor catre asociatie.
    Corespunde entitatii 'Invoice' din diagrama de clase si ER diagram.
    """

    def __init__(self, id: int, amount: float, date: str, supplier_id: int):
        self.id = id
        self.amount = amount
        self.date = date
        self.supplier_id = supplier_id

    @staticmethod
    def get_all() -> list:
        """
        Returneaza toate facturile cu numele furnizorului (JOIN).
        Fiecare element: (id, supplier_name, amount, date)
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, s.name, i.amount, i.date
                FROM Invoices i
                JOIN Suppliers s ON i.supplier_id = s.id
                ORDER BY i.date DESC;
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print("Eroare la preluare facturi:", e)
            return []

    @staticmethod
    def adauga(supplier_id: int, amount: float, date: str) -> bool:
        """Adauga o factura noua."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Invoices (amount, date, supplier_id) VALUES (%s, %s, %s)",
                (amount, date, supplier_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Eroare la adaugare factura:", e)
            return False

    @staticmethod
    def get_total() -> float:
        """Returneaza suma totala a tuturor facturilor."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM Invoices;")
            total = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return float(total)
        except Exception as e:
            print("Eroare la calcul total facturi:", e)
            return 0.0
