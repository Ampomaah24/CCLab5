from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host="redis", port=6379)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
)
cur = conn.cursor()

# Create the 'hits' table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS hits (
    id SERIAL PRIMARY KEY,
    count INT
)
""")
conn.commit()

@app.route("/")
def home():
    # Increment Redis hit count
    count = r.incr("hits")

    # Insert visit into PostgreSQL
    cur.execute("INSERT INTO hits (count) VALUES (%s)", (count,))
    conn.commit()

    return f"This page has been visited {count} times."


if __name__ == "__main__":
    app.run(host="0.0.0.0")
