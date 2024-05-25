from flask import Flask, jsonify, request
#from MentorMatchy.__init__ import app
import json, os, psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv
app = Flask(__name__)

# GENERIC

@app.route('/<string:email>', methods=['GET'])
def get_by_email(email: str):
    cursor.execute(
       'SELECT * FROM USERS WHERE EMAIL_ADDRESS = (%s);',
       {email}
    )
    return jsonify(cursor.fetchone()), 201

@app.route('/user',methods=['GET'])
def retrieve_all():
    cursor.execute("SELECT * FROM USERS;")
    return jsonify(cursor.fetchall()), 201

@app.route('/user', methods=['POST'])
def post_user():
    try:
        user = json.loads(request.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    if not _validate_user(user):
        return jsonify({'error': 'Invalid employee properties'}), 400
    vals = [f"'{val}'" for val in user.values()]
    print(', '.join(user.keys()))
    print(', '.join(vals))

    cursor.execute("""
                    INSERT INTO USERS
                   (%s)
                   VALUES(%s)
                   """, (
                       AsIs(', '.join(user.keys())),
                       AsIs(', '.join(vals))
                    ))
    database.commit()

    return '', 201, {'location': f'/{user['EMAIL_ADDRESS']}'}

# MENTORS

@app.route('/mentors', methods=['GET'])
def get_all_mentors():
    cursor.execute("SELECT * FROM USERS WHERE MATCHING_ROLE = 'Mentor';")
    return jsonify(cursor.fetchall()), 201
   
def _validate_user(mentor_info) -> bool:
   return True

# MENTEES


if __name__ == '__main__':
   load_dotenv()

   database = psycopg2.connect(os.getenv('DATABASE_URL'))
   cursor = database.cursor()
   app.run(debug=True, port=5000)
   cursor.close()
   database.close()