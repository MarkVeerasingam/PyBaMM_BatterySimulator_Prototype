from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/simulation_finished', methods=['POST'])
def simulation_finished():
    try:
        # Extract data from the request
        data = request.json

        print(f"Received JSON payload: {data}")

        # Extract the combined data from the 'result' key
        combined_data = data.get('result', [])

        print("Received combined data from simulation:")
        for data_point in combined_data:
            print(data_point)

        # Return a response
        return jsonify({
            "status": "success",
            "message": "Data received and logged",
            "combined_data": data.get("result")  
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}",
        })

if __name__ == "__main__":
    app.run(debug=True, port=3000)
