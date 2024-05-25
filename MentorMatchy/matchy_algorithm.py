import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def retrieve_user_info():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS WHERE ROLE="Mentor" AND ISMATCHED="FALSE"')
    entries = cursor.fetchall()
    print(entries)
    cursor.close()
    conn.close()
    return entries

def create_dicts(users_entries):
    mentor_dict = {}
    for i in users_entries:
        profile_list = i[0:2].append(i[3:14])
        mentor_dict[i[2]] = profile_list

def main():
    mentor_entries = retrieve_user_info()
    create_dicts(mentor_entries)


# Numerical scale of 1 to 10
# List of all your users and O(n^2) do double for loop and compare every user against one another and 
# then you calculate the absolute value differences between each personality value; do some summation of the differences; 
# one with least differences with each other is a better match

if __name__ == "__main__":
    main()