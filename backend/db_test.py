import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="project_db",
    user="postgres",
    password="pavan@2805"
)

cur = conn.cursor()
cur.execute("SELECT version();")
result = cur.fetchone()

print("Connected! Postgres version:")
print(result)

cur.close()
conn.close()