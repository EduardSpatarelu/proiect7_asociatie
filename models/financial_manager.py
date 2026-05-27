import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db_connection

class FinancialManager:
    """
    Gestioneaza calculele financiare lunare ale asociatiei.
    Corespunde entitatii 'FinancialManager' din diagrama de clase.
    Calculeaza cota fiecarui apartament si genereaza raportul lunar.
    """

    def calculate_monthly_fee(self, apartment_id: int, room_count: int,
                               resident_count: int, total_invoices: float,
                               total_salaries: float, total_rooms: int) -> float:
        """
        Calculeaza cota lunara de intretinere pentru un apartament.
        Formula:
        suma = ((total_facturi + total_salarii) / total_camere) * camere_apartament * (nr_locatari * 0.5)
        """
        if total_rooms == 0:
            return 0.0
        suma = ((total_invoices + total_salaries) / total_rooms) \
               * room_count * (resident_count * 0.5)
        return round(suma, 2)

    def generate_report(self) -> dict:
        """
        Genereaza raportul lunar complet pentru toate apartamentele.

        Returneaza:
          - total_invoices: suma totala facturi
          - total_salaries: suma totala salarii
          - raport: lista de dicts per apartament cu suma_plata
        """
        total_invoices = 0.0
        total_salaries = 0.0
        raport_final = []

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verifica daca toate datele sunt disponibile
            cursor.execute("SELECT COUNT(*) FROM Invoices;")
            nr_facturi = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM waterconsumption;")
            nr_apa = cursor.fetchone()[0]

            if nr_facturi == 0 or nr_apa == 0:
                cursor.close()
                conn.close()
                return {
                    "status": "error",
                    "message": "Date lipsa: facturi sau indici apa neintroduse.",
                    "total_invoices": 0.0,
                    "total_salaries": 0.0,
                    "raport": []
                }

            # Fetch total facturi
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM Invoices;")
            total_invoices = float(cursor.fetchone()[0])

            # Fetch total salarii
            cursor.execute("SELECT COALESCE(SUM(salariu_brut), 0) FROM Employees;")
            total_salaries = float(cursor.fetchone()[0])

            # Fetch total camere
            cursor.execute("SELECT COALESCE(SUM(room_count), 0) FROM Apartments;")
            total_rooms = int(cursor.fetchone()[0])

            # Loop apartamente
            cursor.execute(
                "SELECT id, room_count, resident_count FROM Apartments ORDER BY id;"
            )
            apartamente = cursor.fetchall()

            for apt in apartamente:
                apt_id, apart_rooms, residents = apt
                suma = self.calculate_monthly_fee(
                    apt_id, apart_rooms, residents,
                    total_invoices, total_salaries, total_rooms
                )
                raport_final.append({
                    "id": apt_id,
                    "camere": apart_rooms,
                    "locatari": residents,
                    "suma_plata": suma
                })

            cursor.close()
            conn.close()

        except Exception as e:
            print("Eroare la generare raport:", e)

        return {
            "status": "ok",
            "total_invoices": total_invoices,
            "total_salaries": total_salaries,
            "raport": raport_final
        }
