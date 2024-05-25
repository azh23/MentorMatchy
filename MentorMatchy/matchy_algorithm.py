from user_info import user
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def retrieve_user_info():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS")
    entries = cursor.fetchall()
    print(entries)
    cursor.close()
    conn.close()
    return entries

def filter_matched(entries):
    new_entries_list = []
    for i in entries:
        if i[5] is False:
            new_entries_list.append(i)
    return new_entries_list

def create_dicts(users_entries):
    mentor_dict = {}
    if users_entries[9] == 'Mentor':
        profile_list = []
        profile_list.extend()
        mentor_dict[users_entries[6]] = profile_list
    elif users_entries[9] == 'Mentee':
        profile_list = []
        profile_list.extend()
        mentor_dict[users_entries[6]] = profile_list


def create_mentee_dict(profile_entries, users_entries):
    pass

def main():
    users_entries = retrieve_user_info()
    # removes previously matched users
    users_entries = filter_matched(users_entries)
    # filters based on role 
    create_dicts(users_entries)


# Numerical scale of 1 to 10
# List of all your users and O(n^2) do double for loop and compare every user against one another and 
# then you calculate the absolute value differences between each personality value; do some summation of the differences; 
# one with least differences with each other is a better match

if __name__ == "__main__":
    main()