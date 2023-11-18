from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/simulation_finished', methods=['POST'])
def simulation_finished():
    # Extract data from the request
    data = request.json

    # Print the received data to the console
    print("Received data from simulation:", data)

    # Return a response
    return jsonify({"status": "success", "message": "Data received and logged"})

if __name__ == "__main__":
    app.run(debug=True, port=3000)