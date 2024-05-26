from flask import Flask, jsonify, request
#from MentorMatchy.__init__ import app
import json, os, psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv
from matchy_algorithm import return_match_emails
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app)

# GENERIC

tarazhang1@gmail.com
# Retrieve users by email.
@app.route('/email/<string:email>', methods=['GET'])
def get_by_email(email: str):
    # * ASK WHEN THEY GET TO THIS POINT: If *no* person exists on the email address, 
    # are they ok with null being returned?
    return sql_to_json("SELECT * FROM USERS WHERE EMAIL_ADDRESS = %s", (email, )), 201

# Retrieve all users.
@app.route('/user',methods=['GET'])
def retrieve_all():
    return sql_to_json("SELECT * FROM USERS;"), 201

# Insert a user.
@app.route('/user', methods=['POST'])
@flask_cors.cross_origin()
def post_user():
    try:
        user = json.loads(request.data)
        vals = [f"'{val}'" if type(val) == str else str(val) for val in user.values()]

        cursor.execute("""
                    INSERT INTO USERS (%s)
                    VALUES(%s)
                    """, 
                    (
                        AsIs(', '.join(user.keys())),
                        AsIs(', '.join(vals))
                    ))
        database.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    location = jsonify({'location': f'/{user['EMAIL_ADDRESS']}'})
    location.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify({'location': f'/{user['EMAIL_ADDRESS']}'}), 201

# Retrieve all mentors.
@app.route('/mentors', methods=['GET'])
def get_all_mentors():
    return sql_to_json("SELECT * FROM USERS WHERE MATCHING_ROLE = 'Mentor'"), 201

# Retrieve all mentees.
@app.route('/mentees', methods=['GET'])
def get_all_mentees():
    return sql_to_json("SELECT * FROM USERS WHERE MATCHING_ROLE = 'Mentee'"), 201

# Retrieve a list of potential matches.
@app.route('/matchy/<string:email>', methods=['GET'])
def match(email):
    cursor.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = %s",
                   (email,))
    status = cursor.fetchone()
    if status is None:
        return jsonify({'error': 'Invalid email address'}), 400
    print(status)
    match_emails = return_match_emails(status, is_mentor = (status[8] == 'Mentor'))

    matched_candidate_list = []

    for email in match_emails:
        cursor.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = %s;", (email,))
        matched_users = [dict((cursor.description[i][0], value) \
        for i, value in enumerate(row)) for row in cursor.fetchall()]
        matched_candidate_list.extend(matched_users)

    return jsonify(matched_candidate_list), 201

@app.route('/matched/mentor/<string:email>/mentee/<string:email2>', methods = ['PUT'])
def confirm_match(email, email2):
    cursor.execute("UPDATE USERS SET ISMATCHED = TRUE WHERE EMAIL_ADDRESS = %s",
                   (email, ))
    database.commit()

    cursor.execute("UPDATE USERS SET MATCHED_EMAIL = %s WHERE EMAIL_ADDRESS = %s",
                   (email2, email))
    database.commit()

    cursor.execute("UPDATE USERS SET ISMATCHED = TRUE WHERE EMAIL_ADDRESS = %s",
                   (email2, ))
    database.commit()

    cursor.execute("UPDATE USERS SET MATCHED_EMAIL = %s WHERE EMAIL_ADDRESS = %s",
                   (email, email2))
    database.commit()
    return jsonify({'status': 'Success'}), 201

# Converts SQL query into JSON.
def sql_to_json(query: str, parameters = ()):
    cursor.execute(query, parameters)
    users = [dict((cursor.description[i][0], value) \
    for i, value in enumerate(row)) for row in cursor.fetchall()]
    return jsonify(users)

if __name__ == '__main__':
   load_dotenv()

   database = psycopg2.connect(os.getenv('DATABASE_URL'))
   cursor = database.cursor()
   app.run(debug=True, port=3000)
   cursor.close()
   database.close()

# fetch("localhost:3000/path").then(result=> {
#   do something with result
# })