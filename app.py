import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS STUDENT (ID INT PRIMARY KEY, NAME STRING)")
conn.commit()

cursor.execute("INSERT INTO STUDENT (ID, NAME) VALUES (2, 'Happy')")
conn.commit()

cursor.execute("SELECT * FROM STUDENT")
rows = cursor.fetchall()
print(rows)
cursor.close()
conn.close()

#pip install --upgrade pip setuptools wheel