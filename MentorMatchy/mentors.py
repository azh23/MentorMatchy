from flask import Flask, jsonify, request
from __init__ import app
import json

mentors = [ { 'id': 1, 'name': 'Ashley' }]

@app.route('/mentors/<string:email>')
def get_mentee_by_email():
    sql_request = {'SELECT *',
                  'FROM person'
                   'WHERE email = (:email)' }
    # ...

@app.route('/mentors', methods=['GET'])
def get_mentors():
 return jsonify(mentors)

