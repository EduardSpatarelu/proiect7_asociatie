from proiect7_asociatie.database import get_db_connection


class Apartment:
    """
    Reprezinta un apartament din bloc.
    Corespunde entitatii 'Apartment' din diagrama de clase.
    """

    def __init__(self, id: int, room_count: int,
                 resident_count: int, current_debt: float = 0.0):
        self.id = id
        self.room_count = room_count
        self.resident_count = resident_count
        self.current_debt = current_debt

    def update_residents(self, new_resident_count: int) -> bool:
        """Actualizeaza numarul de locatari al apartamentului."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Apartments SET resident_count = %s WHERE id = %s",
                (new_resident_count, self.id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.resident_count = new_resident_count
            return True
        except Exception as e:
            print("Eroare la actualizare locatari:", e)
            return False

    @staticmethod
    def get_all() -> list:
        """Returneaza toate apartamentele din baza de date."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, room_count, resident_count FROM Apartments ORDER BY id;"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Apartment(r[0], r[1], r[2]) for r in rows]
        except Exception as e:
            print("Eroare la preluare apartamente:", e)
            return []

    @staticmethod
    def adauga(room_count: int, resident_count: int) -> bool:
        """Adauga un apartament nou in sistem."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Apartments (room_count, resident_count) VALUES (%s, %s)",
                (room_count, resident_count)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Eroare la adaugare apartament:", e)
            return False

    @staticmethod
    def get_ids() -> list:
        """Returneaza doar ID-urile apartamentelor (pentru dropdown-uri)."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Apartments ORDER BY id;")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [r[0] for r in rows]
        except Exception as e:
            print("Eroare la preluare ID-uri apartamente:", e)
            return []

    @staticmethod
    def get_total_rooms() -> int:
        """Returneaza suma totala a camerelor din toate apartamentele."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(room_count), 0) FROM Apartments;")
            total = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return int(total)
        except Exception as e:
            print("Eroare la calcul total camere:", e)
            return 0


class Locatar:
    """
    Reprezinta un locatar asociat unui apartament.
    Corespunde entitatii 'Locatar' din diagrama de clase.
    """

    def __init__(self, nume_complet: str, apartament_id: int,
                 este_proprietar: bool = False):
        self.nume_complet = nume_complet
        self.apartament_id = apartament_id
        self.este_proprietar = este_proprietar

    def vizualizeaza_intretinere(self) -> float:
        """Returneaza cota de intretinere a apartamentului asociat."""
        from proiect7_asociatie.models.financial_manager import FinancialManager
        fm = FinancialManager()
        report = fm.generate_report()
        for entry in report.get("raport", []):
            if entry["id"] == self.apartament_id:
                return entry["suma_plata"]
        return 0.0

    def introdu_index_apa(self, index_nou: int, data: str) -> bool:
        """Inregistreaza un index de apa nou pentru apartament."""
        return WaterConsumption.adauga(self.apartament_id, index_nou, data)

    def vizualizeaza_istoric_plati(self) -> list:
        """Returneaza istoricul de plati al apartamentului."""
        from proiect7_asociatie.models.payment import Payment
        return Payment.get_by_apartment(self.apartament_id)

    def plateste_online(self, suma: float, data: str) -> bool:
        """Inregistreaza o plata online pentru apartament."""
        from proiect7_asociatie.models.payment import Payment
        return Payment.adauga(self.apartament_id, suma, data)


class WaterConsumption:
    """
    Reprezinta consumul de apa inregistrat pentru un apartament.
    Corespunde entitatii 'WaterConsumption' din ER diagram.
    """

    def __init__(self, id: int, apartament_id: int,
                 index_value: int, date: str):
        self.id = id
        self.apartament_id = apartament_id
        self.index_value = index_value
        self.date = date

    @staticmethod
    def get_all() -> list:
        """Returneaza toate inregistrarile de consum apa."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, apartament_id, index_value, date "
                "FROM waterconsumption ORDER BY date DESC;"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print("Eroare la preluare consum apa:", e)
            return []

    @staticmethod
    def adauga(apartament_id: int, index_value: int, data: str) -> bool:
        """Adauga un nou index de consum apa."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO waterconsumption (apartament_id, index_value, date) "
                "VALUES (%s, %s, %s)",
                (apartament_id, index_value, data)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Eroare la adaugare index apa:", e)
            return False
