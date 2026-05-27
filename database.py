import psycopg2

def get_db_connection():
    """Returneaza o conexiune activa la baza de date PostgreSQL."""
    conn = psycopg2.connect(
        dbname="asociatie_db",
        user="postgres",
        password="1133",
        host="localhost",
        port="5432"
    )
    return conn
