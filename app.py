import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))

cursor = conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS USERS (
               EMAIL_ADDRESS TEXT PRIMARY KEY, 
               FIRST_NAME TEXT, 
               LAST_NAME TEXT, 
               PRONOUNS TEXT, 
               AGE INT, 
               ABOUT_ME TEXT, 
               INTERESTS TEXT, 
               INDUSTRY TEXT, 
               ADDRESS TEXT, 
               PHOTO_LINK TEXT,
               MATCHED_EMAIL TEXT)
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS PROFILE (
               EMAIL_ADDRESS STRING PRIMARY KEY, 
               WORK_STYLE INT, 
               FOCUS_STYLE INT, 
               PROBLEM_STYLE INT, 
               LEAD_STYLE INT, 
               EXPERIENCE INT, 
               ISMATCHED BOOLEAN)
               """)
conn.commit()


# cursor.execute("""
#                INSERT INTO USERS 
#                (EMAIL_ADDRESS, FIRST_NAME, LAST_NAME, PRONOUNS, AGE, ABOUT_ME) 
#                VALUES('connieay@uci.edu', 'Connie', 'Yang', 'she/her', 18, 'I like to collect plushies.')
#                """)
# conn.commit()

# cursor.execute("""
#                INSERT INTO PROFILE
#                (EMAIL_ADDRESS, WORK_STYLE, FOCUS_STYLE, PROBLEM_STYLE, LEAD_STYLE, EXPERIENCE, ISMATCHED) 
#                VALUES('connieay@uci.edu', 5, 5, 5, 5, 5, TRUE)
#                """)
# conn.commit()

cursor.execute("SELECT * FROM PROFILE")
rows = cursor.fetchall()
print(rows)
cursor.close()
conn.close()