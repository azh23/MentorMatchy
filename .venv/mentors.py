from flask import Flask, jsonify, request
import json

app = Flask(__name__)

mentors = [ { 'id': 1, 'name': 'Ashley' }]

@app.route('/mentors', methods=['GET'])
def get_mentors():
 return jsonify(mentors)