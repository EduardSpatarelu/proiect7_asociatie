import psycopg2

def calculeaza_intretinerea():
    # 1. Conectarea la baza de date
    conn = psycopg2.connect(
        dbname="asociatie_db",
        user="postgres", 
        password="1234", 
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    try:
        # 2. Extragem Total Facturi
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM Invoices;")
        total_invoices = float(cursor.fetchone()[0])

        # 3. Extragem Total Salarii
        cursor.execute("SELECT COALESCE(SUM(salariu_brut), 0) FROM Employees;")
        total_salaries = float(cursor.fetchone()[0])

        # 4. Extragem Total Camere în Asociație
        cursor.execute("SELECT COALESCE(SUM(room_count), 0) FROM Apartments;")
        total_rooms = int(cursor.fetchone()[0])

        if total_rooms == 0:
            print("Eroare: Nu există apartamente înregistrate sau numărul total de camere este 0.")
            return

        print(f"--- REZUMAT LUNAR ---")
        print(f"Total Facturi: {total_invoices} RON")
        print(f"Total Salarii: {total_salaries} RON")
        print(f"Total Camere: {total_rooms}")
        print(f"---------------------\n")

        # 5. Extragem apartamentele și aplicăm formula
        cursor.execute("SELECT id, room_count, resident_count FROM Apartments ORDER BY id;")
        apartamente = cursor.fetchall()

        for apt in apartamente:
            apt_id = apt[0]
            apart_rooms = apt[1]
            residents = apt[2]

            # FORMULA REQ-41
            suma = ((total_invoices + total_salaries) / total_rooms) * apart_rooms * (residents * 0.5)

            print(f"Apartamentul {apt_id}:")
            print(f" - Camere: {apart_rooms}, Locatari: {residents}")
            print(f" - Sumă de plată: {suma:.2f} RON\n")

    except Exception as e:
        print(f"A apărut o eroare la calcul: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    calculeaza_intretinerea()