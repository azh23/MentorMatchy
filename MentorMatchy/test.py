from flask import Flask, jsonify, request
from MentorMatchy.__init__ import app
#from main import app
import json

print('Test file is running')
#app = Flask(__name__)
database = ''
employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }]
nextEmployeeId = 4

@app.route('/')
def hello():
    return '<h1>Hello, World</h1>'

@app.route('/employees', methods=['GET'])
def get_employees():
 print('Get employees ran')
 return jsonify(employees)

@app.route('/employees', methods = ['POST'])
def create_employee():
   global nextEmployeeId
   employee = json.loads(request.data)
   employee['id'] = nextEmployeeId
   nextEmployeeId += 1
   employees.append(employee)

   return '', 201, {'location': f'/employees/{employee["id"]}'}

if __name__ == '__main__':
   app.run(debug=True)