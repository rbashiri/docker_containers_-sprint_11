from flask import Flask, jsonify
try:
    import psycopg2
except ImportError:
    psycopg2 = None
import os

app = Flask(__name__)

# Database connection settings
DB_HOST = "database"  # This is the service name from docker-compose.yml
DB_NAME = "myapp"
DB_USER = "user"
DB_PASSWORD = "password"

def get_db_connection():
    """Connect to the PostgreSQL database"""
    if psycopg2 is None:
        print("psycopg2 module not available")
        return None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route("/")
def home():
    return "Hello from Python app connected to PostgreSQL!"

@app.route("/users")
def get_users():
    """Get all users from the database"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, created_at FROM users ORDER BY id")
        users = cur.fetchall()
        cur.close()
        conn.close()

        # Convert to list of dictionaries
        user_list = []
        for user in users:
            user_list.append({
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "created_at": user[3].isoformat() if user[3] else None
            })

        return jsonify({"users": user_list})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add-user/<name>/<email>")
def add_user(name, email):
    """Add a new user"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": f"User {name} added with ID {user_id}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)