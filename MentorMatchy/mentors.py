from flask import Flask, jsonify, request
from __init__ import app
import json

# MENTORS

mentors = [ { 'id': 1, 'name': 'Ashley' }]

@app.route('/mentors/<str:email>', methods=['GET'])
def get_mentor_by_email(email: str):
    sql_request = {'SELECT *',
                  'FROM person'
                   'WHERE email = (:email)' }
    # ...

@app.route('/mentors/', methods=['POST'])
def create_mentor():
   mentor = json.loads(request.data)
   if not _validate_mentor(mentor):
      return jsonify({'error': 'Invalid employee properties'}), 400
   
def _validate_mentor(mentor_info) -> bool:
   pass

@app.route('/mentors/<str:email>/matchy', methods=['GET'])
def match_a_mentor(email: str):
   pass

@app.route('/mentors', methods=['GET'])
def get_mentors():
 return jsonify(mentors)

# MENTEES