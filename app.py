import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))

cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS USERS (
               FIRST_NAME TEXT, 
               LAST_NAME TEXT, 
               EMAIL_ADDRESS TEXT PRIMARY KEY, 
               PRONOUNS TEXT, 
               ABOUT_ME TEXT, 
               INTERESTS TEXT, 
               INDUSTRY TEXT, 
               PHOTO_LINK TEXT,
               MATCHING_ROLE TEXT,
               WORK_STYLE INT,
               FOCUS_STYLE INT,
               SOLVE_PROBLEM_STYLE INT,
               LEAD_STYLE INT,
               EXPERIENCE INT,
               ISMATCHED BOOLEAN,
               MATCHED_EMAIL TEXT)
               """)
conn.commit()


# cursor.execute("""
#                INSERT INTO USERS 
#                (EMAIL_ADDRESS, FIRST_NAME, LAST_NAME, PRONOUNS, AGE, ABOUT_ME) 
#                VALUES('connieay@uci.edu', 'Connie', 'Yang', 'she/her', 18, 'I like to collect plushies.')
#                """)
# conn.commit()


cursor.execute("SELECT * FROM USERS")
rows = cursor.fetchall()
print(rows)
cursor.close()
conn.close()
