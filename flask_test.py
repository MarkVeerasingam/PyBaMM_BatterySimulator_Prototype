import pybamm
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/simulate')
def simulate_battery():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(port=8084)
