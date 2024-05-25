from flask import Flask
app = Flask(__name__)
import test

print('main is running')

if __name__ == '__main__':
    app.run(debug=True)
