from flask import Flask, jsonify, request
#from MentorMatchy.__init__ import app
import json, os, psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv
app = Flask(__name__)

# GENERIC

# Retrieve users by email.
@app.route('/<string:email>', methods=['GET'])
def get_by_email(email: str):
    cursor.execute(
       "SELECT * FROM USERS WHERE EMAIL_ADDRESS = %s;",
       (email,)
    )

    # * ASK WHEN THEY GET TO THIS POINT: If *no* person exists on the email address, 
    # are they ok with null being returned?
    return jsonify(cursor.fetchone()), 201

# Retrieve all users.
@app.route('/user',methods=['GET'])
def retrieve_all():
    cursor.execute("SELECT * FROM USERS;")
    return jsonify(cursor.fetchall()), 201

# Insert a user.
@app.route('/user', methods=['POST'])
def post_user():
    try:
        user = json.loads(request.data)
        vals = [f"'{val}'" for val in user.values()]

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

    return '', 201, {'location': f'/{user['EMAIL_ADDRESS']}'}

# Retrieve all mentors.
@app.route('/mentors', methods=['GET'])
def get_all_mentors():
    cursor.execute("SELECT * FROM USERS WHERE MATCHING_ROLE = 'Mentor';")
    return jsonify(cursor.fetchall()), 201

# Retrieve all mentees.
@app.route('/mentees', methods=['GET'])
def get_all_mentees():
    cursor.execute("SELECT * FROM USERS WHERE MATCHING_ROLE = 'Mentee';")
    return jsonify(cursor.fetchall()), 201


if __name__ == '__main__':
   load_dotenv()

   database = psycopg2.connect(os.getenv('DATABASE_URL'))
   cursor = database.cursor()
   app.run(debug=True, port=5000)
   cursor.close()
   database.close()