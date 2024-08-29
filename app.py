from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
import psycopg2
from flask_cors import CORS  # Import CORS

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app, origins=["https://petowner-front3.onrender.com"])
# Apply CORS to the entire app

# Manually define the PostgreSQL connection details
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


# Get the list of all pets
@app.route("/pets/", methods=["GET"])
def pets_list():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, age, image FROM pets;")
    pets = cur.fetchall()
    cur.close()
    conn.close()

    # Convert list of dictionaries to a single dictionary with individual key-value pairs
    pets_dict = {}
    for pet in pets:
        pets_dict[pet["id"]] = {
            "name": pet["name"],
            "age": pet["age"],
            "image": pet["image"],
        }

    return jsonify(pets_dict)


# Add a new pet
@app.route("/pets", methods=["POST"])
def add_pet():
    new_pet = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pets (name, age, image) VALUES (%s, %s, %s) RETURNING id;",
        (new_pet["name"], new_pet["age"], new_pet["image"]),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"result": "Pet added successfully", "id": new_id})


# Get a single pet by ID
@app.route("/pets/<int:id>", methods=["GET"])
def single_pet(id):
    conn = get_db_connection()
    cur = conn.cursor(
        cursor_factory=RealDictCursor
    )  # Use RealDictCursor to get dictionary results
    cur.execute("SELECT id, name, age, image FROM pets WHERE id = %s;", (id,))
    pet = cur.fetchone()
    cur.close()
    conn.close()

    if pet:
        return jsonify(
            {
                "id": pet["id"],
                "name": pet["name"],
                "age": pet["age"],
                "image": pet["image"],
            }
        )
    else:
        return jsonify({"result": "Pet not found"}), 404


# Delete a pet by ID
@app.route("/pets/<int:id>", methods=["DELETE"])
def delete_pet(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pets WHERE id = %s RETURNING id;", (id,))
    deleted_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted_id:
        return jsonify({"result": "Pet deleted successfully"}), 200
    else:
        return jsonify({"result": "Pet not found"}), 404


# Update a pet by ID
@app.route("/pets/<int:id>", methods=["PUT"])
def update_pet(id):
    updated_pet = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE pets SET name = %s, age = %s, image = %s WHERE id = %s RETURNING id;",
        (updated_pet["name"], updated_pet["age"], updated_pet["image"], id),
    )
    updated_id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if updated_id:
        return jsonify({"result": "Pet updated successfully"}), 200
    else:
        return jsonify({"result": "Pet not found"}), 404


# Run the app only if this script is executed (not imported)
if __name__ == "__main__":
    app.run(debug=True)
