# db_connection.py
import psycopg2

# Define your PostgreSQL connection details
DB_HOST = "dpg-cr6ugig8fa8c738266jg-a.oregon-postgres.render.com"  # Example: 'localhost' or 'db.render.com'
DB_NAME = "pets_db_updated"  # Example: 'petsdb'
DB_USER = "pets_db_updated_user"  # Example: 'admin'
DB_PASSWORD = "3p3QpkvFMvnQvMjjAbW88Ls0lDSiNRKC"  # Example: 'yourpassword'
DB_PORT = "5432"  # The default PostgreSQL port is 5432


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    return conn
