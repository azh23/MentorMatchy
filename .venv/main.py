from flask import Flask

app = Flask(__name__)

import test

if __name__ == '__main__':
    app.run(debug=True)
   #Flask('test').run(debug=True)
   #Flask('mentors').run(debug=True)