# create_tables.py
from db_connection import get_db_connection


def create_pets_table():
    conn = get_db_connection()
    cur = conn.cursor()

    # SQL statement to create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pets (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INTEGER NOT NULL,
        image TEXT
    );
    """

    # Execute the SQL command
    cur.execute(create_table_query)
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    print("Pets table created successfully.")


# Run the function to create the table
if __name__ == "__main__":
    create_pets_table()
