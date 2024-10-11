from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)

conn = psycopg2.connect(
    host="db",
    database="database",
    user="user",
    password="password"
)

cur = conn.cursor()

@app.route("/")
def home():
    count = r.incr("hits")
    cur.execute("INSERT INTO hits (count) VALUES (%s)", (count,))
    conn.commit()
    return f"This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
