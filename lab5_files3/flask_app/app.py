from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

# Redis connection
r = redis.Redis(host="redis", port=6379)

# PostgreSQL connection
conn = psycopg2.connect(
    host="db",
    database="postgres_db",
    user="root",
    password="root"
)

cur = conn.cursor()

@app.route('/')
def home():

    redis_count = r.incr("hits")

 
    cur.execute("INSERT INTO hits (count) VALUES (%s)", (redis_count,))
    conn.commit()

    
    cur.execute("SELECT COUNT(*) FROM hits;")
    pg_count = cur.fetchone()[0]


    return f"This page has been run {count} times via Redis and {postgres_count} times in PostgreSQL."
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

